"""
    map.py
    This module contains classes for maps. It has a relationship with the jars. A map can contain multiple jars.
    Jars can't be on multiple maps!
"""

__author__ = "Dermul Bart"

from HornetTracker import db
from sqlalchemy.exc import IntegrityError


class Map(db.Model):
    """
    map_name= is the name of the site where you have plotted jars.
    """
    __tablename__ = "map"

    _id = db.Column(db.Integer, primary_key=True)
    map_name = db.Column(db.String(20), unique=True, nullable=False)
    latitude = db.Column(db.Float(15), unique=True, nullable=False)
    longitude = db.Column(db.Float(15), unique=True, nullable=False)
    jar_id = db.relationship(
        'Hornet',
        backref='map',
        cascade="all, delete"
    )

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
               f"jar_id:{self.jar_id})"

    # GLOBAL var for this class

    # CREATE
    def create(self):
        do_i_exist = Map.find_one_by_name(map_name=self.map_name)
        if do_i_exist:
            print(f"The item for map name: {self.map_name} exists")
            pass
        else:
            db.session.add(self)
            db.session.commit()
        return

    # READ
    @classmethod
    def list(cls):
        return cls.query.all()

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
