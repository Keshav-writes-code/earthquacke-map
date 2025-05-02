from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("map.html")


cnx = mysql.connector.connect(user="root", password="user", host="127.0.0.1")
cursor = cnx.cursor(dictionary=True)


@app.route("/get_data")
def get_data():
    cursor.execute("use earthquake")
    cursor.execute("SELECT * from records_log ORDER BY time DESC limit 100")
    data = cursor.fetchall()
    return data
