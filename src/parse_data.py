import logging
import re
from typing import Optional, Dict, Union

from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.CRITICAL)


def parse_html_title(html_content: str) -> Optional[str]:
    soup = BeautifulSoup(html_content, "html.parser")
    title = soup.title

    return title.string if title else None


def extract_vessel_info(html_content: str) -> Optional[Dict[str, Union[str, int]]]:
    vessel_info = parse_html_title(html_content)
    if not vessel_info:
        logging.info("No title found in html content.")
        return

    pattern = re.compile(r'Ship\s*(\w+).*IMO\s*(\d+).*MMSI\s*(\d+).*Call\s*sign\s*(\w+)')
    pattern_match = pattern.search(vessel_info)

    if not pattern_match:
        logging.info("No vessel data found in parsed html content.")
        return

    vessel_data = {
        'name': pattern_match.group(1),
        'imo': int(pattern_match.group(2)),
        'mmsi': int(pattern_match.group(3)),
        'callsign': pattern_match.group(4)
    }
    return vessel_data
