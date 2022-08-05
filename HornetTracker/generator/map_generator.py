import copy
from HornetTracker.hornets.models.hornet import Hornet
from HornetTracker.map.models.map import Map
import folium
from folium import plugins


def generate_map(map_data: dict):

    new_map = Map.find_one_by_name(map_data["map_name"])
    print(new_map)
    center = [new_map.latitude, new_map.longitude]

    m = folium.Map(location=center, zoom_start=13)

    for jar in new_map.jar_id:

        myjar = copy.deepcopy(jar.__dict__)
        location = [myjar['latitude'], myjar['longitude']]

        tooltip = "Click For information"

        folium.Marker(location,
                      popup=f'<b>JarName:{myjar["jar_name"]}'f'\n NrSightings:{myjar["nr_of_sightings"]}</b>',
                      tooltip=tooltip,
                      icon=folium.Icon(color="red", icon="bee")).add_to(m)

        folium.Circle(location=tuple(location),
                      radius=myjar["average_distance"],
                      color="#3186cc",
                      # fill=False,
                      # fill_color="#3186cc"
                      ).add_to(m)

        plugins.SemiCircle(location=tuple(location),
                           radius=myjar["average_distance"],
                           direction=myjar["heading"],
                           arc=2,
                           fill=True).add_to(m)

        m.save("./HornetTracker/templates/map.html")

    return m._repr_html_()


