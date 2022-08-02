# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import Figure, JavascriptLink

from folium.map import Marker
from folium.utilities import validate_location

from jinja2 import Template


class SemiCircle(Marker):
    """
    Creates a Semicircle plugin to append into a map with
    Map.add_plugin.
    Use (direction and arc) or (startAngle and stopAngle)
    Parameters
    ----------
    location: tuple of length 2, default None
        The latitude and longitude of the marker.
        If None, then the middle of the map is used.
    radius: int, default 0
        Radius of semicircle
    direction: int, default 0
        Heading of direction angle value between 0 and 360 degrees
    arc: int, default 0
        Heading of arc angle value between 0 and 360 degrees.
    startAngle: int, default 0
        Heading of the start angle value between 0 and 360 degrees
    stopAngle: int, default 0
        Heading of the stop angle value between 0 and 360 degrees.
    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                if ({{this.direction}} || {{this.arc}}) {
                    var {{this.get_name()}} = L.semiCircle(
                        [{{this.location[0]}},{{this.location[1]}}],
                        {radius:{{this.radius}},
                        fill: {{this.fill}},
                        fillColor:'{{this.fill_color}}',
                        fillOpacity: {{this.fill_opacity}},
                        color: '{{this.color}}',
                        opacity: {{this.opacity}}
                        }).setDirection({{this.direction}},{{this.arc}})
                        .addTo({{this._parent.get_name()}});
                } else if ({{this.startAngle}} || {{this.stopAngle}}) {
                    var {{this.get_name()}} = L.semiCircle(
                        [{{this.location[0]}},{{this.location[1]}}],
                        {radius:{{this.radius}},
                        fill: {{this.fill}},
                        fillColor:'{{this.fill_color}}',
                        fillOpacity: {{this.fill_opacity}},
                        color: '{{this.color}}',
                        opacity: {{this.opacity}},
                        startAngle:{{this.startAngle}}, 
                        stopAngle:{{this.stopAngle}}
                        })
                        .addTo({{this._parent.get_name()}});
                }
            {% endmacro %}
            """)

    def __init__(self,
                location,
                radius=0,
                fill = True,
                fill_color='#3388ff',
                fill_opacity = 0.5,
                color = '#3388ff',
                opacity = 1,
                direction=0,
                arc=0,
                startAngle=0,
                stopAngle=0, **kwargs):

        super(SemiCircle, self).__init__( validate_location(location), **kwargs)
        self._name = 'SemiCircle'
        self.radius = radius
        if fill == True:
            self.fill = 'true'
        else: self.fill = 'false'
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.color = color
        self.opacity = opacity
        self.direction = direction
        self.arc = arc
        self.startAngle = startAngle
        self.stopAngle = stopAngle
        self.fill_color = fill_color
        self.kwargs = json.dumps(kwargs)

    def render(self, **kwargs):
        super(SemiCircle, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('http://jieter.github.io/Leaflet-semicircle/Semicircle.js'),
name='semicirclejs')