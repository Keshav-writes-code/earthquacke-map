import time
import mysql.connector
from lib.db import setup_db
from lib.usgs import get_usgs_data

cnx = mysql.connector.connect(user="root", password="user", host="127.0.0.1")
cursor = cnx.cursor()


def sync_data():
    # NOTE: Data Fetching
    data = get_usgs_data()

    # NOTE: Pushing to DB
    setup_db("earthquake", cursor)
    values = [(d["mag"], d["place"], d["time"]) for d in data]

    cursor.executemany(
        "INSERT INTO `records_log` (magnitude, place, time) VALUES(%s, %s, %s)", values
    )
    cnx.commit()


def main():
    # NOTE: Push Data from API to DB every 10 Minutes
    interval = 2
    try:
        while True:
            time.sleep(interval)
            sync_data()
            print("Data Pulled ")
    except KeyboardInterrupt:
        print("Program Exited")

    # NOTE: Close DB Connection
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
