"""
    observation.py
    This module contains classes for Observations
    Relationship to JARS "Hornets"
"""

__author__ = "Dermul Bart"

from HornetTracker import db
from sqlalchemy.exc import IntegrityError
from HornetTracker.jars.models.jar import Jar
from datetime import datetime
from folium import plugins


class Observation(db.Model):
    # CHECK UNUSABLE var for this class
    MAX_HEADING = 360
    MAX_DISTANCE = 1000

    __tablename__ = "observation"

    _id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float(15), unique=False, nullable=False)
    longitude = db.Column(db.Float(15), unique=False, nullable=False)
    _average_distance = db.Column(db.Integer, unique=False, nullable=False)
    _heading = db.Column(db.Integer, unique=False, nullable=False)
    jar_id = db.Column(db.Integer, db.ForeignKey("jar._id"))
    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    # __init__
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 average_distance: int,
                 heading: int):

        assert type(longitude) == float, "Longitude must be a type Float"
        assert type(latitude) == float, "Latitude must be a type Float"
        assert type(average_distance) == int, "Average distance must be an integer"
        assert type(heading) == int, "Heading must be an integer"

        self.latitude = latitude
        self.longitude = longitude
        self._average_distance = average_distance
        self._heading = heading

    # REPR
    def __repr__(self):
        return f"{self.__class__.__name__}(_id: {self._id}, " \
               f"latitude:{self.latitude}," \
               f"longitude:{self.longitude}," \
               f"average_distance:{self._average_distance}," \
               f"heading:{self._heading}," \
               f"jar_id:{self.jar_id}," \
               f"date:{self.date})"


    @property
    def average_distance(self):
        return self._average_distance

    @average_distance.setter
    def average_distance(self, value):
        if value > Observation.MAX_DISTANCE:
            raise ValueError("An average distance larger than 1000m is not a usable observation")
        if isinstance(value, str):
            raise ValueError("An average distance must be integer")
        self._average_distance = value

    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, value):
        if value > Observation.MAX_HEADING:
            raise ValueError("A heading can't be larger than 360degrees")
        if isinstance(value, str):
            raise ValueError("A heading must be integer")
        self._heading = value

    # CREATE
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    # READ
    @classmethod
    def list(cls):
        return cls.query.order_by(cls.date).all()

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
        _jar = cls.find_by_db_id(jar["_id"])
        if jar:
            _jar.nr_of_sightings = jar["nr_of_sightings"]
            _jar.average_distance = jar["average_distance"]
            _jar.heading = jar["heading"]
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
    def bind_to_jar(cls, **kwargs):
        theobservation = cls.find_by_db_id(kwargs["observation_id"])
        thejar = Jar.find_by_db_id(kwargs["jar_id"])
        try:
            if thejar and theobservation:
                theobservation.jar_id = thejar._id
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"ISSUES with binding to the jar: {e}")

    #FILTERS
    @classmethod
    def filter_by_latitude(cls, part):
        print(part)
        mylist = []
        mylist.append(part)
        filter_list = [cls.latitude.contains(x) for x in mylist]
        result = cls.query.filter_by()
        print(result)
        return result

    # FILTERS
    @classmethod
    def filter_by_longitude(cls, part):
        print(part)
        result = cls.query.filter_by(longitude=part).all()
        print(result)
        return result

    # FILTERS
    @classmethod
    def filter_by_date(cls, part):
        print(part)
        all = cls.query.all()

        result = cls.query.filter_by(date=part).all()
        print(result)
        return result
