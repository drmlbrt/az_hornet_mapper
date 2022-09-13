import copy

import flask

from HornetTracker.hornets.models.hornet import Hornet
from HornetTracker.map.models.map import Map
import folium
from folium import plugins
from folium import features
from folium.features import ClickForMarker
from folium.features import ClickForMarker, LatLngPopup
import clipboard

import jinja2

template_jinja = u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent("" + e.latlng.lat.toFixed(4) + "," +
                                    "" + e.latlng.lng.toFixed(4))
                        .openOn({{this._parent.get_name()}});
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """

def generatormap(*args, **kwargs):
    """This must receive a dict that contains at least the kwargs long and lat"""
    if isinstance(kwargs, dict):
        center = [kwargs["latitude"], kwargs["longitude"]]

    m = folium.Map(location=center, zoom_start=16)

    mypersonal_popup = features.LatLngPopup()
    mypersonal_popup._template = jinja2.Template(template_jinja)

    m.add_child(mypersonal_popup)


    plugins.MeasureControl().add_to(m)

    return m

def base_map():
    m = generatormap(**{"latitude":50.800097891802515, "longitude":4.423601625815788})
    plugins.LocateControl(auto_start=False).add_to(m)
    return m._repr_html_()


def generate_map(map_data: dict):
    map = Map.find_one_by_name(map_data["map_name"])

    if map is not None:
        m = generatormap(**map.__dict__)

        for jar in map.jar_id:
            myjar = copy.deepcopy(jar.__dict__)
            location = [myjar['latitude'], myjar['longitude']]

            tooltip = "Click For information"

            folium.Marker(location,
                          popup=f'<b>JarName:{myjar["jar_name"]}'f'\n</b>',
                          tooltip=tooltip,
                          icon=folium.Icon(color="red", icon="bee")).add_to(m)

            for observation in jar.observation_id:
                print(observation)

                # folium.Circle(location=tuple(location),
                #               radius=observation.average_distance,
                #               color="#3186cc",
                #               # fill=False,
                #               # fill_color="#3186cc"
                #               ).add_to(m)

                plugins.SemiCircle(location=tuple(location),
                                   radius=observation.average_distance,
                                   direction=observation.heading,
                                   arc=3,
                                   fill=True).add_to(m)

        return m._repr_html_()
    else:
        m = generatormap(**map_data)
        return m._repr_html_()



