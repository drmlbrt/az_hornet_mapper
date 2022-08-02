__author__ = "Dermul Bart"
__copyright__ = "Copyright 2022 - ask before you participate"
__credits__ = ["Dermul Bart"]
__license__ = "GNU"
__version__ = "1"
__maintainer__ = "Dermul Bart"
__email__ = "bart.dermul@gmail.com"
__status__ = "Production"

from flask import Flask, render_template, url_for, redirect
import folium
import pandas as pd
from folium import plugins

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/change_csv")
def csv_changer():
    return render_template("csv_changer.html")


@app.route("/map")
def mapper():
    lures = pd.read_csv('./tracking_data/sample_data.csv')
    # view the dataset
    print(lures.head())

    center = [50.969114, 3.733650]
    map_jars = folium.Map(location=center, zoom_start=16)

    for index, jar in lures.iterrows():
        location = [jar['latitude'], jar['longitude']]
        folium.Marker(location,
                      popup=f'JarName:{jar["jar"]}'f'\n NrSightings:{jar["nr_of_sightings"]}').add_to(map_jars)

        folium.Circle(location,
                      radius=jar["average_distance"]).add_to(map_jars)

        plugins.SemiCircle(location=location,
                           radius=jar["average_distance"],
                           direction=jar["heading_direction"],
                           arc=2,
                           opacity=0.5,
                           fill_color="red",
                           color="red",
                           fill=True).add_to(map_jars)
        map_jars.save("./templates/map.html")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
