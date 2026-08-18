import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError
import logger  # configures root logger
import logging

log = logging.getLogger(__name__)


def fetch_player_data(uid):
    url = f"https://enka.network/api/uid/{uid}/"
    headers = {"User-Agent": "genshin-build-tracker/1.0 (project)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        log.info(f"Successfully fetched player data for UID: {uid}")
    except Timeout as t:
        log.error(f"enka.network took too long to respond: {t}")
        raise
    except ConnectionError as c:
        log.error(f"Error connecting to enka.network: {c}")
        raise
    except HTTPError as h:
        log.error(f"enka.network responded with an error: {h}")
        raise

    return data
