import sqlite3
from sqlite3 import Connection


def create_connection() -> Connection:
    return sqlite3.connect(r"db\vessel_info.db")

def create_vessel_in_database(data: tuple):
    # Creates or updates vessel in database
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO vessels (imo, vessel, callsign, mmsi)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(imo) DO UPDATE SET
            vessel=excluded.vessel,
            callsign=excluded.callsign,
            mmsi=excluded.mmsi;
        ''', data)
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"An error occurred while connecting to database or executing query: {e}")
        conn.close()


def count_vessels_in_db() -> str:
    conn = create_connection()
    cursor = conn.cursor()

    count = cursor.execute("SELECT COUNT(imo) FROM vessels")
    count = count.fetchone()
    conn.commit()
    conn.close()

    return ''.join([str(x) for x in count])
