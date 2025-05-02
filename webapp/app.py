from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("map.html")


cnx = mysql.connector.connect(user="root", password="user", host="127.0.0.1")
cursor = cnx.cursor(dictionary=True)
cursor.execute("use earthquake")


@app.route("/get_data")
def get_data():
    # Get Query Parameters
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    if start_time == "undefined" or end_time == "undefined":
        cursor.execute("SELECT * from records_log ORDER BY time DESC limit 100")
    else:
        print(start_time, end_time)
        query = """
        SELECT * 
        FROM records_log 
        WHERE time BETWEEN %s AND %s
        ORDER BY time DESC 
        LIMIT 500
        """
        cursor.execute(query, (start_time, end_time))
    data = cursor.fetchall()
    return data
