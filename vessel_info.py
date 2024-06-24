from bs4 import BeautifulSoup

from src.webdriver import setup_driver
from src.output import init_program, print_dict_info, print_final_info
from src.vessel_database import count_vessels_in_db, create_vessel_in_database
from src.utility import (create_dict_from_list, get_max_key_value, find_regex_matches_for_imo,
                         find_regex_matches_for_mmsi, find_regex_matches_for_callsign)


def main() -> None:
    """

    :return: None
    """

    vessel = init_program(count_vessels_in_db()).strip().lower()
    if not vessel:
        return

    # Important to have this exact line to produce reliable results
    url = f'https://www.google.com/search?q=container+ship+"{vessel}"+call+sign+imo+mmsi+site:marinetraffic.com'

    # Webdriver to launch headless Edge browser
    with setup_driver() as driver:
        driver.get(url)
        data = driver.page_source

    soup = BeautifulSoup(data, 'html.parser')

    # Finds lists of regex matches
    soup_str = str(soup)
    imo_list = find_regex_matches_for_imo(soup_str)
    mmsi_list = find_regex_matches_for_mmsi(soup_str)
    callsign_list = find_regex_matches_for_callsign(soup_str)

    # From lists to dicts
    imo_dict = create_dict_from_list(imo_list)
    mmsi_dict = create_dict_from_list(mmsi_list)
    callsign_dict = create_dict_from_list(callsign_list)

    # Pretty print dicts with all information found
    print_dict_info(vessel, imo_dict, mmsi_dict, callsign_dict)

    # Gets the highest occurrence of keywords
    vessel = vessel.upper()
    imo: int = get_max_key_value(imo_dict)
    mmsi: int = get_max_key_value(mmsi_dict)
    callsign: str = get_max_key_value(callsign_dict)

    # Creates or updates in database, then print final result
    status = create_vessel_in_database((imo, vessel, callsign, mmsi))
    if status:
        print_final_info(vessel, imo, mmsi, callsign)


if __name__ == '__main__':
    main()
