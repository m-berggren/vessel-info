from typing import Optional, Dict, Union

from src.parse_data import extract_vessel_info
from src.selenium_chrome import get_information_from_chrome_search
from src.vessel_database import create_vessel_in_database, count_vessels_in_db


def main() -> None:
    print(f"-----------------Create vessel in database------------------\n"
          f"Type the name of the vessel you wish to add to the database.\n"
          f"Upper or lower case letters does not matter.\n"
          f"There are currently {count_vessels_in_db()} vessels in database.")
    vessel_name = input("Type the name here: ")
    print("Now we wait a few seconds.")

    html_content = get_information_from_chrome_search(vessel_name)
    if not html_content:
        print(f"Vessel {vessel_name.upper()} not found. Try search for a new vessel.")
        return
    vessel_info = extract_vessel_info(html_content)

    name = vessel_info.get('name')
    imo = vessel_info.get('imo')
    callsign = vessel_info.get('callsign')
    mmsi = vessel_info.get('mmsi')

    print(
        f"\n"
        f"NAME: {name.upper()}\n"
        f"IMO: {imo}\n"
        f"CALLSIGN: {callsign}\n"
        f"MMSI: {mmsi}\n"
    )

    data = (imo, name, callsign, mmsi)
    create_vessel_in_database(data)
    print("Vessel created or updated in database.")


if __name__ == '__main__':
    main()
