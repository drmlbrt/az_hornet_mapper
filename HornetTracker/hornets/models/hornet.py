from HornetTracker import db
from sqlalchemy.exc import IntegrityError
from HornetTracker.map.models.map import Map


class Hornet(db.Model):
    __tablename__ = "hornet"

    _id = db.Column(db.Integer, primary_key=True)
    jar_name = db.Column(db.String(20), unique=True, nullable=False)
    latitude = db.Column(db.Float(15), unique=True, nullable=False)
    longitude = db.Column(db.Float(15), unique=True, nullable=False)
    nr_of_sightings = db.Column(db.Integer, unique=False, nullable=False)
    average_distance = db.Column(db.Integer, unique=False, nullable=False)
    heading = db.Column(db.Integer, unique=False, nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey("map._id"))

    # __init__
    def __init__(self, jar_name: str,
                 latitude: int,
                 longitude: int,
                 nr_of_sightings: int,
                 average_distance: int,
                 heading: int):
        self.jar_name = jar_name
        self.latitude = latitude
        self.longitude = longitude
        self.nr_of_sightings = nr_of_sightings
        self.average_distance = average_distance
        self.heading = heading

    # REPR
    def __repr__(self):
        return f"{self.__class__.__name__}(_id: {self._id}, " \
               f"jar_name:{self.jar_name}," \
               f"latitude:{self.latitude}," \
               f"longitude:{self.longitude}," \
               f"nr_of_sightings:{self.nr_of_sightings}," \
               f"average_distance:{self.average_distance}," \
               f"heading:{self.heading}," \
               f"map_id:{self.map_id})"

    # GLOBAL var for this class

    # CREATE
    def create(self):
        do_i_exist = Hornet.find_one_by_name(jar_name=self.jar_name)
        if do_i_exist:
            print(f"The item 'Hornet' for jar name: {self.jar_name} exists")
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
    def find_one_by_name(cls, jar_name):
        return cls.query.filter_by(jar_name=jar_name).first()

    # UPDATE
    @classmethod
    def update(cls, jar: dict):
        _jar = cls.find_one_by_name(jar["jar_name"])
        print("Entering Update Method in Hornet")
        print(jar)
        if jar:
            _jar.latitude = jar["latitude"]
            _jar.longitude = jar["longitude"]
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
    def bind_to_map(cls, bind_jar_to_map: dict):
        thejar = cls.find_one_by_name(bind_jar_to_map["jar_name"])
        print(thejar)
        themap = Map.find_one_by_name(bind_jar_to_map["map_name"])
        print(themap)
        if thejar and themap:
            thejar.map_id = themap._id
            db.session.commit()
            return True
        else:
            return False
