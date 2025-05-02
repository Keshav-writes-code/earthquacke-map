import datetime
import time
import mysql.connector
from lib.db import setup_db
from lib.usgs import get_usgs_data

cnx = mysql.connector.connect(user="root", password="user", host="127.0.0.1")
cursor = cnx.cursor()


def sync_data(last_sync_time: datetime.datetime):
    # NOTE: Data Fetching
    data = get_usgs_data(last_sync_time.isoformat())

    # NOTE: Pushing to DB
    setup_db("earthquake", cursor)
    values = [
        (d["mag"], d["place"], d["longitude"], d["latitude"], d["time"]) for d in data
    ]
    print(f"{datetime.datetime.now().strftime('%-I:%M:%S %p')} : ", end="")
    if not values:
        print("On Latest Changes")
    else:
        print("Data Pulled ")

    cursor.executemany(
        "INSERT INTO `records_log` (magnitude, place, longitude, latitude, time) VALUES(%s, %s, %s, %s, %s)",
        values,
    )
    cnx.commit()


def main():
    # NOTE: Push Data from API to DB every 2 Seconds
    last_sync_time = datetime.datetime.now() - datetime.timedelta(55)
    interval = 2
    try:
        while True:
            time.sleep(interval)
            sync_data(last_sync_time)
            last_sync_time = datetime.datetime.now()
    except KeyboardInterrupt:
        print("Program Exited")

    # NOTE: Close DB Connection
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
