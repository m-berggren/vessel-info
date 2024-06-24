from collections import defaultdict
import html

from bs4 import BeautifulSoup

from src.output import init_program, print_dict_info, print_final_info
from src.vessel_database import count_vessels_in_db, create_vessel_in_database
from src.webdriver import setup_driver
from src.utility import (create_dict_from_list, string_found, date_found, find_regex_matches, get_max_key_value,
                         find_regex_matches_for_imo,
                         find_regex_matches_for_mmsi, find_regex_matches_for_callsign)


def main() -> None:
    """

    :return: None
    """

    vessel = init_program(count_vessels_in_db()).strip().lower()
    if not vessel:
        return

    url = f"https://www.google.com/search?q=container+vessel+{vessel}+imo+call+sign+mmsi+marinetraffic"

    # Webdriver to launch headless Edge browser
    with setup_driver() as driver:
        driver.get(url)
        data = driver.page_source

    soup = BeautifulSoup(data, 'html.parser')
    # content = soup.find(id="res")
    content = soup.find(id="rso")

    # Find the div with id "rso"
    rso_div = soup.find('div', {'id': 'rso'})

    # Define the possible values of data-snf
    data_dnf_values = ['nke7rc', 'x5WNvb', 'oyZ5Hb']

    text = ""
    # Extract and print the span information from each target div
    for value in data_dnf_values:
        target_divs = rso_div.find_all('div', {'data-snf': value})
        for div in target_divs:
            #spans = div.find_all('span')
            span = div.find('span')
            print(span.text)
            """for span in spans:
                text += span.text
                print(span.text)"""
            text += span.text

    soup_str = str(soup) + str(content) + text
    imo_list = find_regex_matches_for_imo(soup_str)
    mmsi_list = find_regex_matches_for_mmsi(soup_str)
    callsign_list = find_regex_matches_for_callsign(soup_str)

    imo_dict = create_dict_from_list(imo_list)
    mmsi_dict = create_dict_from_list(mmsi_list)
    callsign_dict = create_dict_from_list(callsign_list)

    print_dict_info(vessel, imo_dict, mmsi_dict, callsign_dict)

    vessel = vessel.upper()
    imo: int = get_max_key_value(imo_dict)
    mmsi: int = get_max_key_value(mmsi_dict)
    callsign: str = get_max_key_value(callsign_dict)

    status = create_vessel_in_database((imo, vessel, callsign, mmsi))
    """if status:
        print_final_info(vessel, imo, mmsi, callsign)"""

    print_final_info(vessel, imo, mmsi, callsign)


if __name__ == '__main__':
    main()
