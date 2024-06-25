import re
import urllib.parse


def _normalize_vessel_name(name: str) -> str:
    if not name:
        return str()
    # Decode URL-encoded characters
    decoded_name = urllib.parse.unquote(name)
    # Remove delimiters (spaces, underscores, hyphens)
    normalized_name = re.sub(r'[\s_\-]', '', decoded_name)
    return normalized_name.lower()


def compare_vessel_names(name1: str, name2: str) -> bool:
    return _normalize_vessel_name(name1) == _normalize_vessel_name(name2)
