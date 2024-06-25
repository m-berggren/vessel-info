from typing import Optional


def format_line(label: str, value: str | int = None) -> str:
    if value:
        string = f"    {label}: {value}"
    else:
        string = f"{label}:"
    return string


def init_program(vessel_count: str) -> Optional[str]:
    print(f"{'            CREATE VESSEL IN DATABASE'}\n"
          f"\n"
          f"Type the name of the vessel you wish to add to the database.'\n"
          f"Upper or lower case letters does not matter.\n"
          f"There are currently {vessel_count} vessels stored.\n"
          )

    vessel_name = input(f'Type the name below (or exit with Enter):\n')
    if not vessel_name:
        return

    print('\nPlease wait a few seconds while gathering information...\n')
    return vessel_name


def print_final_info(vessel: str, imo: int, mmsi: int, callsign: str) -> None:
    print(f"{format_line(f'{vessel} is created/updated in database')}\n"
          f"{format_line(f'''{'VESSEL':9}''', vessel)}\n"
          f"{format_line(f'''{'IMO':9}''', imo)}\n"
          f"{format_line(f'''{'MMSI':9}''', mmsi)}\n"
          f"{format_line(f'''{'CALLSIGN':9}''', callsign)}\n"
          f"\n"
          f'APPLICATION IS FINISHED.\n')


def print_incomplete_info(vessel: str, imo: int, mmsi: int, callsign: str) -> None:
    print(f"{format_line(f'{vessel} not created, information missing')}\n"
          f"{format_line(f'''{'VESSEL':9}''', vessel if vessel else 'N/A')}\n"
          f"{format_line(f'''{'IMO':9}''', imo if imo else '-')}\n"
          f"{format_line(f'''{'MMSI':9}''', mmsi if mmsi else '-')}\n"
          f"{format_line(f'''{'CALLSIGN':9}''', callsign if callsign else '-')}\n"
          f"\n"
          f'APPLICATION IS FINISHED.\n')