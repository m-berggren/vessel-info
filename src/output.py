from typing import Optional


def format_line(label: str, value: str | int = None) -> str:
    if value:
        string = f"    {label}: {value}"
    else:
        string = f" {label}"
    return f"{string:<120}"


def init_program(vessel_count: str) -> Optional[str]:
    print(f"{format_line('            CREATE VESSEL IN DATABASE')}\n"
          f"{format_line("")}\n"
          f"{format_line('Type the name of the vessel you wish to add to the database.')}\n"
          f"{format_line('Upper or lower case letters does not matter.')}\n"
          f"{format_line(f"There are currently {vessel_count} vessels stored.")}\n"
          f"{format_line("")}")

    vessel_name = input(f"{format_line("Type the name below (or exit with Enter):")}\n ")
    if not vessel_name:
        return

    print(format_line(""))
    print(format_line("Please wait a few seconds while gathering information..."))
    print(format_line(""))
    return vessel_name


def print_dict_info(vessel: str, d1: dict, d2: dict, d3: dict) -> None:
    print(f"{format_line(f"Number of tags found for {vessel.upper()}:")}")
    print(f"{format_line(f"{'IMO':9}", f"{dict(d1)}")}")
    print(f"{format_line(f"{'MMSI':9}", f"{dict(d2)}")}")
    print(f"{format_line(f"{'CALLSIGN':9}", f"{dict(d3)}")}")
    print(format_line(""))


def print_final_info(vessel: str, imo: int, mmsi: int, callsign: str) -> None:
    print(f"{format_line(f"{vessel} is created/updated in database:")}\n"
          f"{format_line(f"{'VESSEL':9}", vessel)}\n"
          f"{format_line(f"{'IMO':9}", imo)}\n"
          f"{format_line(f"{'MMSI':9}", mmsi)}\n"
          f"{format_line(f"{'CALLSIGN':9}", callsign)}\n"
          f"{format_line("")}\n"
          f"{format_line("APPLICATION IS FINISHED.")}\n")
