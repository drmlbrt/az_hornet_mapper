from marshmallow import Schema, fields, post_dump, pre_load, post_load, pre_dump
from HornetTracker.jars.schemas.s_jar import Hornet_D

class Map_D(Schema):
    class Meta:
        ordered = True

    _id = fields.Int(dump_only=True)
    map_name = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    jar_id = fields.List(fields.Nested(Hornet_D()))

    @pre_dump
    def pre_dump_map(self, data, **kwargs):
        print(f"####################PRE DUMP MAP #### {data}")
        return data

    @post_dump
    def dump_map(self, data, **kwargs):
        print(f"********************POST DUMP DATA : MAP  : {data}")
        data = {"map_name": data["map_name"],
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "jars": data["jar_id"]}
        return data


class Map_L(Schema):
    class Meta:
        ordered = True

    _id = fields.Int()
    map_name = fields.Str()
    latitude = fields.Int()
    longitude = fields.Int()

    @pre_load
    def serialize_metadata(self, data, **kwargs):
        return data
