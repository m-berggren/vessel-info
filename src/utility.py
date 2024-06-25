import re
from collections import defaultdict
from typing import List, Union, Tuple, Optional


def find_regex_matches_for_imo(html: str) -> list:
    regex = r"[Ii][Mm][Oo][</em>),\s:]*([0-9]{7})"
    return re.findall(regex, html)


def find_regex_matches_for_mmsi(html: str) -> list:
    regex = r"[Mm][Mm][Ss][Ii][:</em>),\s]*([0-9]{9})"
    return re.findall(regex, html)


def find_imo_matches(imo: str, html: str):
    return re.findall(imo, html)


def find_regex_matches_for_callsign(html: str) -> list:

    callsign_us_regex = r"[Cc]all\s*[Ss]ign[</em>),\s:]*([A-Z0-9]*[A-Z][A-Z0-9]*)(?=Gross|[.,\s]|$)"
    callsign_se_regex = r"[Aa]nropssignal[),\s:]*([A-Z0-9]+(?<![\.]))"
    callsign_fr_regex = r"[Ii]ndicatif\s*[Dd]'[Aa]ppel[),\s:]*([A-Z0-9]+(?<![\.]))"

    callsigns_us = re.findall(callsign_us_regex, html)
    callsigns_se = re.findall(callsign_se_regex, html)
    callsigns_fr = re.findall(callsign_fr_regex, html)

    return callsigns_us + callsigns_se + callsigns_fr


def get_vessel(url: str) -> Optional[str]:
    match = re.search(r'(?<=vessel:)[\w%]+', url)

    perc = '%20'
    uscore = '_'

    if match:
        match = match.group()
        match.replace(perc, ' ')
        match.replace(uscore, ' ')

    return match


def get_imo(url: str) -> int:
    match = re.search(r'(?<=imo:)[0-9]+', url)
    return int(match.group()) if match else 0


def get_mmsi(url: str) -> int:
    match = re.search(r'(?<=mmsi:)[0-9]+', url)
    return int(match.group()) if match else 0


def get_callsign(text: str) -> str:
    match = re.search(r'[Cc]all\s*[Ss]ign[</em>),\s:]*([A-Z0-9]*[A-Z][A-Z0-9]*)', text)
    return match.group(1) if match else ""


def create_dict_from_list(strings: list) -> Optional[dict]:
    if not strings:
        return

    count_dict = defaultdict(int)

    for value in strings:
        count_dict[value] += 1

    return dict(count_dict)


def get_max_key_value(d: dict) -> Union[int, str]:
    """
    For each key in the dictionary the d.get method is called,
    which retrieves the value associated with that key.
    :return: Key with the highest value.
    """
    if not d:
        return 0
    return max(d, key=d.get)
