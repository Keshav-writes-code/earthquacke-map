from django.http import JsonResponse
from django.shortcuts import render
import mysql.connector


# Create your views here.
def home_view(request):
    return render(request, "home/index.html")


cnx = mysql.connector.connect(user="root", password="user", host="127.0.0.1")
cursor = cnx.cursor(dictionary=True)
cursor.execute("use earthquake")


def get_data(request):
    if request.method == "GET":
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        if start_time == "undefined" or end_time == "undefined":
            cursor.execute("SELECT * from records_log ORDER BY time DESC limit 100")
        else:
            query = """
            SELECT * 
            FROM records_log 
            WHERE time BETWEEN %s AND %s
            ORDER BY time DESC 
            LIMIT 500
            """
            cursor.execute(query, (start_time, end_time))
        data = cursor.fetchall()
        return JsonResponse(data, safe=False)
        data = {"status": "ok", "message": "Hello from Django App!"}
        return JsonResponse(data)
