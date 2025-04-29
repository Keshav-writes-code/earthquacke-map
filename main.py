from lib.usgs import get_usgs_data


def main():
    # NOTE: Data Fetching
    data = get_usgs_data()
    )
    data = response.json()
    mag = data["features"][2]["properties"]["mag"]

    print(mag)


if __name__ == "__main__":
    main()
