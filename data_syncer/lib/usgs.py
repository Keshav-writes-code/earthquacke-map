from typing import TypedDict
import requests
import datetime


class Filtered_Feature(TypedDict):
    mag: str
    place: str
    time: datetime.datetime
    longitude: float
    latitude: float


def get_usgs_data(start_date: str):
    parameters = {
        "format": "geojson",
        "starttime": start_date,
    }
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query", parameters
    )
    data = response.json()
    filtered_features: list[Filtered_Feature] = []
    for feature in data["features"]:
        prop = feature["properties"]
        geo = feature["geometry"]
        time_ms = int(prop["time"]) / 1000
        filtered_feature: Filtered_Feature = {
            "mag": prop["mag"],
            "place": prop["place"],
            "time": datetime.datetime.fromtimestamp(int(time_ms)),
            "longitude": geo["coordinates"][0],
            "latitude": geo["coordinates"][1],
        }
        filtered_features.append(filtered_feature)
    return filtered_features
