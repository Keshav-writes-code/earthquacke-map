import requests


def main():
    parameters = {
        "format": "geojson",
        "starttime": "2014-01-01",
        "endtime": "2014-01-02",
    }
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query", parameters
    )
    data = response.json()
    mag = data["features"][2]["properties"]["mag"]

    print(mag)


if __name__ == "__main__":
    main()
