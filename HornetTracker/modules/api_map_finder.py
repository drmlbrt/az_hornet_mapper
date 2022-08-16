import requests
import json


def mapfinder(form_address: int) -> dict:
    url = f"https://loc.geopunt.be/v4/Location?q={form_address}"

    payload = {}
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        jsonresponse = json.loads(response.text)

        # print(jsonresponse)
        latitude = jsonresponse["LocationResult"][0]["Location"]["Lat_WGS84"]
        # print(latitude)
        longitude = jsonresponse["LocationResult"][0]["Location"]["Lon_WGS84"]
        # print(longitude)
        form_address_format = str(jsonresponse["LocationResult"][0]["FormattedAddress"]).replace(",", "_")

        return {"mapname": form_address_format, "latitude": latitude, "longitude": longitude}

    else:

        return False
