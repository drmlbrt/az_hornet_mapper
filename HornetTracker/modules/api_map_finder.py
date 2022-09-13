import requests
import json
from flask import Flask, render_template, url_for, redirect, Blueprint, flash, request, Response

def  mapfinder(form_address: int) -> dict:
    url = f"https://loc.geopunt.be/v4/Location?q={form_address}"
    payload = {}
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:

            jsonresponse = json.loads(response.text)

            if isinstance(jsonresponse["LocationResult"], list):
                if len(jsonresponse["LocationResult"]) == 1:

                    latitude = jsonresponse["LocationResult"][0]["Location"]["Lat_WGS84"]
                    # print(latitude)
                    longitude = jsonresponse["LocationResult"][0]["Location"]["Lon_WGS84"]
                    # print(longitude)
                    form_address_format = str(jsonresponse["LocationResult"][0]["FormattedAddress"]).replace(",", "_")

                    return {"map_name": form_address_format, "latitude": latitude, "longitude": longitude}

                elif len(jsonresponse["LocationResult"]) == 0:
                    return flash(f"Address does not exist for {form_address}", "warning")

                elif len(jsonresponse["LocationResult"]) > 1:
                    results = []
                    for i in jsonresponse["LocationResult"]:
                        results.append({"Municipality": i['Municipality'], "Street": i['Thoroughfarename']})
                    return flash(f"Got many Results {results}", "warning")
        else:
            return flash(f"Address does not exist for {form_address}", "warning")

    except Exception:
        return flash("Address locator is not available, Alternative is to search manually on the map", "warning")
