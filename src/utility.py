import re
from collections import defaultdict
from typing import List, Union, Tuple, Optional


def find_regex_matches(html: str) -> List[Tuple[str]]:
    """
    Regex function searches for IMO followed by 7 numbers, and/or MMSI followed by 9 numbers and/or variations of
    Call Sign (could be call sign, callsign, Call Sign, Callsign, even French and Swedish versions), followed by arbitrary
    numbers and letters, as some Call Signs use both.
    :return: List of tuples, i.e. [("9223455", , , , , ),].
    """
    pattern = re.compile(
        r"(?<=IMO)[:</em>),\s]*([0-9]{7})|"                     # IMO
        r"(?<=MMSI)[:</em>),?\s]*([0-9]{9})|"                   # MMSI
        r"(?<=[Cc]all [Ss]ign)[:</em>),\s]*([A-Z0-9]+)|"        # Call Sign
        r"(?<=[Cc]all[Ss]ign)[:</em>),\s]*([A-Z0-9]+)|"         # Call Sign #2
        r"(?<=[Aa]nropssignal)[:),\s]*([A-Z0-9]+)|"             # Call Sign (SE)
        r"(?<=[Ii]ndicatif [Dd]'[Aa]ppel)[:),\s]*([A-Z0-9]+)")  # Call Sign (FR)

    pattern = re.compile(r"(?<=IMO)[:<\/em>\),\s]*([0-9]{7})|(?<=MMSI)[:<\/em>\),?\s]*([0-9]{9})|(?<=[Cc]all [Ss]ign)[:<\/em>\),\s]*([A-Z0-9]+)|(?<=[Cc]all[Ss]ign)[:<\/em>\),\s]*([A-Z0-9]+)|(?<=[Aa]nropssignal)[:\),\s]*([A-Z0-9]+)|(?<=[Ii]ndicatif [Dd]'[Aa]ppel)[:\),\s]*([A-Z0-9]+)", flags=re.M)
    return pattern.findall(html)


def find_regex_matches_for_imo(html: str) -> list:
    regex = r"[Ii][Mm][Oo][</em>),\s:]*([0-9]{7})"
    return re.findall(regex, html)


def find_regex_matches_for_mmsi(html: str) -> list:
    regex = r"[Mm][Mm][Ss][Ii][:</em>),\s]*([0-9]{9})"
    return re.findall(regex, html)


def find_regex_matches_for_callsign(html: str) -> list:

    #callsign_us_regex = r"[Cc]all\s*[Ss]ign[</em>),\s:]*([A-Z0-9]+(?<![\.]))"
    callsign_us_regex = r"[Cc]all\s*[Ss]ign[</em>),\s:]*([A-Z0-9]*[A-Z][A-Z0-9]*)(?=Gross|[.,\s]|$)"
    callsign_se_regex = r"[Aa]nropssignal[),\s:]*([A-Z0-9]+(?<![\.]))"
    callsign_fr_regex = r"[Ii]ndicatif\s*[Dd]'[Aa]ppel[),\s:]*([A-Z0-9]+(?<![\.]))"

    callsigns_us = re.findall(callsign_us_regex, html)
    callsigns_se = re.findall(callsign_se_regex, html)
    callsigns_fr = re.findall(callsign_fr_regex, html)

    return callsigns_us + callsigns_se + callsigns_fr


def create_dict_from_list(strings: list) -> Optional[dict]:
    if not strings:
        return

    count_dict = defaultdict(int)

    for value in strings:
        count_dict[value] += 1

    return dict(count_dict)


def date_found(string: str):
    if not string:
        return True
    regex_dates = (r"\b(\d{1,2})\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?"
                   r"|Apr(?:il)?|Maj|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|"
                   r"Sep(?:tember)?|Oct(?:ober)?|Okt(?:ober)?|Nov(?:ember)?|"
                   r"Dec(?:ember)?)\s+(\d{4})\b")
    matches = re.findall(regex_dates, string)
    match_string = bool(matches) if isinstance(matches, list) else False

    return match_string


def string_found(string: str) -> bool:
    if not string:
        return True

    set_string = {'Saknas:', 'Missing:'}
    return string in set_string


def get_max_key_value(d: dict) -> Union[int, str]:
    """
    For each key in the dictionary the d.get method is called,
    which retrieves the value associated with that key.
    :return: Key with the highest value.
    """
    return max(d, key=d.get)
