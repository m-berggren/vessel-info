from typing import List

from bs4 import BeautifulSoup

from src.webparser import get_request
from src.string_parser import compare_vessel_names
from src.output import init_program, print_final_info, print_incomplete_info
from src.utility import get_vessel, get_imo, get_mmsi, get_callsign
from src.vessel_database import count_vessels_in_db, create_vessel_in_database


def get_html_data(vessel_name: str) -> BeautifulSoup:
    url = f'https://www.google.com/search?q=container+ship+"{vessel_name}"+call+sign+imo+mmsi+site:marinetraffic.com'
    response = get_request(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_name_imo_mmsi_list(soup: BeautifulSoup) -> List[str]:
    url_list = []
    yur_class_list = soup.find_all('div', class_='yuRUbf')
    for div in yur_class_list:
        url_list.append(div.a.get('href'))
    return url_list


def get_callsign_list(soup: BeautifulSoup) -> List[str]:
    callsign_list = []
    nke_class_list = soup.find_all('div', {'data-snf': 'nke7rc'})
    for nke_class in nke_class_list:
        callsign_list.append(get_callsign(nke_class.span.text))
    return callsign_list


def main():
    vessel_name = init_program(count_vessels_in_db()).strip().upper()
    soup = get_html_data(vessel_name)

    href_url_list = get_name_imo_mmsi_list(soup)
    callsign_list = get_callsign_list(soup)

    vessel, imo, mmsi, callsign = "", 0, 0, ""

    # Loop through list of URLs to find a match with vessel name and callsign (using enumerate num)
    for num, href_url in enumerate(href_url_list):
        vessel = get_vessel(href_url)
        callsign = callsign_list[num]
        # Compare names and checks if callsign exists
        if compare_vessel_names(vessel, vessel_name) and callsign:
            imo = int(get_imo(href_url))
            mmsi = int(get_mmsi(href_url))
            break

    vessel_name = vessel_name.upper()

    # When callsign is not found, print out incomplete info
    if not callsign:
        print_incomplete_info(vessel_name, imo, mmsi, callsign)
        return

    # Create or update vessel in database, end with printing all complete info
    status = create_vessel_in_database((imo, vessel_name, callsign, mmsi))
    if status:
        print_final_info(vessel_name, imo, mmsi, callsign)


if __name__ == '__main__':
    main()
