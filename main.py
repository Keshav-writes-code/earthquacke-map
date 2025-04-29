import mysql.connector
from mysql.connector import errorcode
from lib.db import TABLES, setup_db
from lib.usgs import get_usgs_data

cnx = mysql.connector.connect(user="root", password="user", host="127.0.0.1")
cursor = cnx.cursor()


def main():
    # NOTE: Data Fetching
    data = get_usgs_data()

    # NOTE: Pushing to DB
    setup_db("earthquake", cursor)
    values = [(d["mag"], d["place"], d["time"]) for d in data]

    cursor.executemany(
        "INSERT INTO `records_log` (magnitude, place, time) VALUES(%s, %s, %s)", values
    )

    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
