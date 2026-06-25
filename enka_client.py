import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError


def fetch_player_data(uid):
    url = f"https://enka.network/api/uid/{uid}/"
    headers = {"User-Agent": "genshin-build-tracker/1.0 (project)"}
    try:
        # API call
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Timeout as t:
        print(f"enka.network took too long to respond: {t}")
        raise
    except ConnectionError as c:
        print(f"Error connecting to enka.network: {c}")
        raise
    except HTTPError as h:
        print(f"enka.network responded with an error: {h}")
        raise

    return data
