from typing import TypedDict
import requests
import datetime


class Filtered_Feature(TypedDict):
    mag: str
    place: str
    time: datetime.datetime


def get_usgs_data():
    parameters = {
        "format": "geojson",
        "starttime": "2014-01-01",
        "endtime": "2014-01-02",
    }
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query", parameters
    )
    data = response.json()
    filtered_features: list[Filtered_Feature] = []
    for feature in data["features"]:
        prop = feature["properties"]
        time_ms = int(prop["time"]) / 1000
        filtered_feature: Filtered_Feature = {
            "mag": prop["mag"],
            "place": prop["place"],
            "time": datetime.datetime.fromtimestamp(int(time_ms)),
        }
        filtered_features.append(filtered_feature)
    return filtered_features
