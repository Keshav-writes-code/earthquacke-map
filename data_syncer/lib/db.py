import mysql.connector
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection

TABLES: dict[str, str] = {}
TABLES["records_log"] = (
    "CREATE TABLE `records_log` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `time` date NOT NULL,"
    "  `magnitude` FLOAT NOT NULL,"
    "  `place` varchar(200) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)


def create_databse(DB_NAME: str, cursor: MySQLCursorAbstract):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )
    except mysql.connector.Error as err:
        print("Failed to Create Database : {}".format(err))
        exit(1)

    return


def setup_db(
    DB_NAME: str,
    cursor: MySQLCursorAbstract,
):
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_databse(DB_NAME, cursor)
            cursor.execute("USE {}".format(DB_NAME))
            for table_name in TABLES:
                schema = TABLES[table_name]
                try:
                    print("Creating table {}: ".format("table_name"), end="")
                    cursor.execute(schema)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("Already Exists")
                    else:
                        print(err.msg)
                else:
                    print("OK")

        else:
            print(err)
            exit(1)
