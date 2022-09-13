"""
    observation.py
    This module contains classes for Observations
    Relationship to JARS "Hornets"
"""

__author__ = "Dermul Bart"

from HornetTracker import db
from sqlalchemy.exc import IntegrityError
from HornetTracker.hornets.models.hornet import Hornet
from datetime import datetime

def currentisotime():
    current_date = datetime.now()
    return current_date.isoformat()

class Observation(db.Model):
    __tablename__ = "observation"

    _id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float(15), unique=False, nullable=False)
    longitude = db.Column(db.Float(15), unique=False, nullable=False)
    average_distance = db.Column(db.Integer, unique=False, nullable=False)
    heading = db.Column(db.Integer, unique=False, nullable=False)
    jar_id = db.Column(db.Integer, db.ForeignKey("hornet._id"))
    date = db.Column(db.DateTime, unique=True, nullable=False, default=datetime.utcnow)

    # __init__
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 average_distance: int,
                 heading: int):
        self.latitude = latitude
        self.longitude = longitude
        self.average_distance = average_distance
        self.heading = heading
        # self.date = currentisotime()

    # REPR
    def __repr__(self):
        return f"{self.__class__.__name__}(_id: {self._id}, " \
               f"latitude:{self.latitude}," \
               f"longitude:{self.longitude}," \
               f"average_distance:{self.average_distance}," \
               f"heading:{self.heading}," \
               f"jar_id:{self.jar_id}," \
               f"date:{self.date})"

    # GLOBAL var for this class

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
        # print("Entering Update Method in Hornet")
        # print(jar)
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
        print(theobservation)

        thejar = Hornet.find_by_db_id(kwargs["jar_id"])
        print(thejar)

        try:
            if thejar and theobservation:

                theobservation.jar_id = thejar._id
                print(theobservation)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"ISSUES with binding to the jar: {e}")
