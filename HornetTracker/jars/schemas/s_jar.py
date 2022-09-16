from marshmallow import Schema, fields, post_dump, pre_load, post_load, pre_dump
from HornetTracker.observations.schemas.s_observation import Observation_D

class Hornet_D(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    jar_name = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    map_id = fields.Int()
    observation_id = fields.List(fields.Nested(Observation_D()))


    @pre_dump
    def pre_dump_hornet(self, data, **kwargs):
        print(f"####################PRE DUMP HORNETS#### {data}")

        return data

    @post_dump
    def dump_hornet(self, data, **kwargs):
        print(f"********************POST DUMP DATA : HORNETS  : {data}")
        data = {"jar_name": data["jar_name"],
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "map": data["map_id"],
                "observations": data["observation_id"]}
        return data


class Hornet_L(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    jar_name = fields.Str()
    latitude = fields.Int()
    longitude = fields.Int()

    @pre_load
    def serialize_metadata(self, data, **kwargs):
        return data