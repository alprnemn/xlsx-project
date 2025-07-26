import argparse
from datetime import datetime
import json

import pandas as pd
import requests
from typing import Dict, List, Optional
from cfg import config

_token_cache = {
    "access_token": None,
}

_columns = ["rnr","gruppe","kurzname","langtext","info","lagerort","labelIds","hu"]

# server.py
def get_access_token() -> str :
    """
    Returns a cached access token or fetches a new one if not cached.
    """

    if _token_cache["access_token"]:
        return _token_cache["access_token"]

    payload = {
        "username": config["USERNAME"],
        "password": config["PASSWORD"]
    }
    headers = {
        "Authorization": f"Basic {config['BASIC_AUTH_TOKEN']}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post("https://api.baubuddy.de/index.php/login",
                                 json=payload,
                                 headers=headers,
                                 timeout=10)
        response.raise_for_status()
        access_token = response.json()["oauth"]["access_token"]
        _token_cache["access_token"] = access_token
        return access_token
    except Exception as e:
        raise RuntimeError("Error occurred while getting access token") from e

def fetch_df_from_external_api() -> pd.DataFrame:
    """
    Fetch vehicle data from external Baubuddy API using Bearer access token and returns pd dataframe.
    """

    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        raise RuntimeError("Error occurred while getting external data") from e

def concat_and_filter_dataframes(df_1: pd.DataFrame, df_2: pd.DataFrame) -> pd.DataFrame:
    """
    This function concatenates two dataframes, removes duplicates based on 'kurzname'(to be unique),
    filters out rows where the 'hu' column is missing and returns dataframe.
    """

    # update data with only substantial columns
    df_1 = df_1[['rnr','gruppe','kurzname','langtext','info','lagerort','labelIds','hu']]

    # concat dataframes
    df_concatenated = pd.concat([df_1, df_2], ignore_index=True)

    # drop duplicates based on kurzname
    df_concatenated = df_concatenated.drop_duplicates(subset='kurzname', ignore_index=True)

    # drop missing values at 'hu' column
    df_concatenated.dropna(subset=['hu'], inplace=True)


    return df_concatenated

def clean_label_id(val):
    """
    This function extracts the first labelId from the 'labelIds' value.
    - If the value is a string, it splits by comma and returns the first part.
    - If the value is NaN, it returns None.
    """
    if pd.isnull(val):
        return None
    if isinstance(val, str):
        return val.split(',')[0].strip()
    return None

def fetch_color_code(label_id: str, access_token: str) -> Optional[str]:
    """
    Fetches the colorCode for a given labelId from the Baubuddy API.
    Returns None if not found or request fails.
    """

    if not label_id:
        return None
    url = f"https://api.baubuddy.de/dev/index.php/v1/labels/{label_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("colorCode")
    except requests.exceptions.RequestException as e:
        print(f"Request error for labelId {label_id}: {e}")

    return None

def fetch_and_add_color_codes(df:pd.DataFrame) -> pd.DataFrame :
    """
    This function fetches color codes from external api using label id and adds color code to new column.
    """
    if not df.empty:
        df['colorCode'] = None

    for idx, row in df.iterrows():
        label_ids_raw = row['labelIds']

        if pd.notna(label_ids_raw):
            label_id = clean_label_id(label_ids_raw)
            if label_id:
                color_code = fetch_color_code(label_id, get_access_token())
                if color_code:
                    df.at[idx, 'colorCode'] = color_code

    return df


# client.py
def parse_args():
    """
    This function parses arguments from the command line and validates:
    - No duplicate keys
    - All keys must be in _columns
    Returns parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog='Client',
        description='Client parser to make excel table',
    )
    parser.add_argument("-k", "--keys", nargs="*", default=[])
    parser.add_argument("-c", "--colored", action="store_true")

    args = parser.parse_args()

    # Check for duplicate keys
    seen = set()
    duplicates = set()
    for key in args.keys:
        if key in seen:
            duplicates.add(key)
        seen.add(key)

    if duplicates:
        parser.error(f"Duplicate keys found: {', '.join(duplicates)}")

    # Check for invalid keys
    invalid = [key for key in args.keys if key not in _columns]
    if invalid:
        parser.error(f"Invalid keys: {', '.join(invalid)}. Valid keys are: {', '.join(_columns)}")

    return args

def upload_csv_and_get_df_from_server(filepath: str, url: str = "http://localhost:8000/upload") -> pd.DataFrame:
    """
    Uploads a CSV file to a given REST API endpoint and parses the JSON response into a pandas DataFrame.
    """
    with open(filepath, "rb") as f:
        res = requests.post(url, files={"file": f})
        res.raise_for_status()
        data = res.json()
        if isinstance(data, dict) and 'data' in data:
            parsed = json.loads(data['data'])
        else:
            parsed = data

        # convert dataframe parsed json data
        df = pd.DataFrame(parsed)

        # sort values by gruppe
        df = df.sort_values("gruppe")

        return df