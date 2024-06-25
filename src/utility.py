import re
from typing import Union, Optional


def get_vessel(url: str) -> Optional[str]:
    match = re.search(r'(?<=vessel:)[\w%]+', url)
    return match.group() if match else ""


def get_imo(url: str) -> int:
    match = re.search(r'(?<=imo:)[0-9]+', url)
    return int(match.group()) if match else 0


def get_mmsi(url: str) -> int:
    match = re.search(r'(?<=mmsi:)[0-9]+', url)
    return int(match.group()) if match else 0


def get_callsign(text: str) -> str:
    match = re.search(r'[Cc]all\s*[Ss]ign[</em>),\s:]*([A-Z0-9]*[A-Z][A-Z0-9]*)', text)
    return match.group(1) if match else ""


def get_max_key_value(d: dict) -> Union[int, str]:
    """
    For each key in the dictionary the d.get method is called,
    which retrieves the value associated with that key.
    :return: Key with the highest value.
    """
    if not d:
        return 0
    return max(d, key=d.get)
