import logging
import pandas as pd
import requests
from typing import Dict, List
from cfg import config

_token_cache = {
    "access_token": None,
}

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

