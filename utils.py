import logging
import pandas as pd
import requests
from typing import Dict
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

def fetch_data_from_external_api() -> pd.DataFrame:
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

