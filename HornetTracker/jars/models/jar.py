"""
    observation.py
    This module contains classes for Jars
"""

__author__ = "Dermul Bart"

from HornetTracker import db
from sqlalchemy.exc import IntegrityError
from HornetTracker.map.models.map import Map
from HornetTracker.modules.workers import datetime
import folium
from folium import plugins


class Jar(db.Model):
    __tablename__ = "jar"

    _id = db.Column(db.Integer, primary_key=True)
    jar_name = db.Column(db.String(60), unique=True, nullable=False)
    latitude = db.Column(db.Float(15), unique=True, nullable=False)
    longitude = db.Column(db.Float(15), unique=True, nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey("map._id"))
    observation_id = db.relationship(
        'Observation',
        backref='jar',
        cascade="all, delete"
    )
    date = db.Column(db.DateTime, unique=True, nullable=False, default=datetime.utcnow)

    # __init__
    def __init__(self, jar_name: str,
                 latitude: float,
                 longitude: float):

        assert type(jar_name) == str, "Jar Name must be string"
        assert type(latitude) == float, "Latitude must be a float"
        assert type(longitude) == float, "Longitude must be a float"

        self.jar_name = jar_name
        self.latitude = latitude
        self.longitude = longitude

    # REPR
    def __repr__(self):
        return f"{self.__class__.__name__}(_id: {self._id}, " \
               f"jar_name:{self.jar_name}," \
               f"latitude:{self.latitude}," \
               f"longitude:{self.longitude}," \
               f"map_id:{self.map_id}," \
               f"observation_id: {self.observation_id}," \
               f"date: {self.date})"

    # GLOBAL var for this class

    # CREATE
    def create(self):
        do_i_exist = Jar.find_one_by_name(jar_name=self.jar_name)
        try:
            if do_i_exist:
                print(f"The item for jar name: {self.jar_name} exists")
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
        return cls.query.order_by(cls.jar_name).all()

    # FIND ONE
    @classmethod
    def find_by_db_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    @classmethod
    def find_one_by_name(cls, jar_name: str):
        return cls.query.filter_by(jar_name=jar_name).first()

    # UPDATE
    @classmethod
    def update(cls, jar: dict):
        _jar = cls.find_one_by_name(jar["jar_name"])
        # print("Entering Update Method in Hornet")
        # print(jar)
        if jar:
            _jar.latitude = jar["latitude"]
            _jar.longitude = jar["longitude"]
            db.session.add(_jar)
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

    # BIND TO MAP
    @classmethod
    def bind_to_map(cls, bind_jar_to_map: dict):
        thejar = cls.find_one_by_name(bind_jar_to_map["jar_name"])

        themap = Map.find_one_by_name(bind_jar_to_map["map_name"])

        if thejar and themap:
            thejar.map_id = themap._id
            db.session.commit()
            return True
        else:
            return False

