"""
    map.py
    This module contains classes for maps. It has a relationship with the jars. A map can contain multiple jars.
    Jars can't be on multiple maps!
"""

__author__ = "Dermul Bart"

from HornetTracker import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import folium
from folium import plugins
from folium import features
import jinja2


class Map(db.Model):
    """
    map_name= is the name of the site where you have plotted jars.
    """

    TEMPLATE_JINJA = u"""
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

    __tablename__ = "map"

    _id = db.Column(db.Integer, primary_key=True)
    map_name = db.Column(db.String(20), unique=True, nullable=False)
    latitude = db.Column(db.Float(15), unique=True, nullable=False)
    longitude = db.Column(db.Float(15), unique=True, nullable=False)
    jar_id = db.relationship(
        'Jar',
        backref='map',
        cascade="all, delete"
    )
    date = db.Column(db.DateTime, unique=True, nullable=False, default=datetime.utcnow)

    # __init__
    def __init__(self, map_name: str,
                 latitude: float,
                 longitude: float):
        self.map_name = map_name
        self.latitude = latitude
        self.longitude = longitude

    # REPR
    def __repr__(self):
        return f"{self.__class__.__name__}(_id: {self._id}, " \
               f"map_name:{self.map_name}," \
               f"latitude:{self.latitude}," \
               f"longitude:{self.longitude}," \
               f"jar_id:{self.jar_id}," \
               f"date: {self.date})"

    # GLOBAL var for this class

    # CREATE
    def create(self):
        do_i_exist = Map.find_one_by_name(map_name=self.map_name)
        try:
            if do_i_exist:
                print(f"The item for Map name: {self.map_name} exists")
                return False
            else:
                try:
                    db.session.add(self)
                    db.session.commit()
                    return True
                except Exception:
                    return False
        except Exception:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    # READ
    @classmethod
    def list(cls):
        return cls.query.order_by(cls.map_name).all()

    # FIND ONE
    @classmethod
    def find_by_db_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    @classmethod
    def find_one_by_name(cls, map_name):
        return cls.query.filter_by(map_name=map_name).first()

    # UPDATE
    @classmethod
    def update(cls, map: dict):
        _map = cls.find_one_by_name(map["map_name"])
        print(map)
        if map:
            _map.latitude = map["latitude"]
            _map.longitude = map["longitude"]
            db.session.commit()
            return True
        else:
            return False

    # DELETE
    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    @classmethod
    def create_map_without_latlng(cls, map_name, *args, **kwargs):
        return cls(map_name=map_name,
                   latitude=None,
                   longitude=None, *args, **kwargs)

    # GENERATE FOLIUM MAP
    @classmethod
    def generate_map(cls, latitude=None, longitude=None, *args, **kwargs):
        """Will generate a map for an instance of object.
        If there is only a marker to printed such as a jar or observation, then call this with a DUMMY NAME
        latitude: for generating marker
        longitude: for generating a marker
        :returns
        a folium object
        """
        if latitude and longitude:
            center = [latitude, longitude]
        else:
            center = [cls.latitude, cls.longitude]
        try:
            m = folium.Map(location=tuple(center), zoom_start=16)
        except Exception as e:
            return {"error": f"{e}"}
        custom_popup = features.LatLngPopup()
        custom_popup._template = jinja2.Template(Map.TEMPLATE_JINJA)
        m.add_child(custom_popup)
        plugins.MeasureControl().add_to(m)
        return m

    @staticmethod
    def generate_map_marker(parent_map,
                            observation=None,
                            jar=None,
                            jar_name=None,
                            latitude=None,
                            longitude=None,
                            average_distance=None,
                            heading=None, *args, **kwargs):
        """get information and create marker information
        :param:
        generated_map: you need toprovide a folium object.
        """
        if jar:
            folium.Marker(location=tuple([latitude, longitude]),
                          popup=f'<b>JarName:{jar_name}''\n</b>',
                          tooltip="Click for information",
                          icon=folium.Icon(color="red", icon="bee")).add_to(parent_map)

        if observation:
            folium.Marker(location=tuple([latitude, longitude]),
                          tooltip="Click for information",
                          popup=
                          f'<b>Heading:{heading}''\n</b>'
                          f'<b>Distance:{average_distance}''\nm</b>',
                          icon=folium.Icon(color="red", icon="bee")).add_to(parent_map)
            plugins.SemiCircle(location=tuple([latitude, longitude]),
                               radius=average_distance,
                               direction=heading,
                               arc=3,
                               fill=True).add_to(parent_map)
        return
