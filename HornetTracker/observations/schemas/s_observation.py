from marshmallow import Schema, fields, post_dump, pre_load, post_load, pre_dump

class Observation_D(Schema):
    class Meta:
        ordered = True

    _id = fields.Int(dump_only=True)
    latitude = fields.Float()
    longitude = fields.Float()
    average_distance = fields.Int()
    heading = fields.Int()
    date = fields.String()
    map_id = fields.Int()


    @pre_dump
    def pre_dump_hornet(self, data, **kwargs):
        print(f"####################PRE DUMP HORNETS#### {data}")

        return data

    @post_dump
    def dump_hornet(self, data, **kwargs):
        print(f"********************POST DUMP DATA : OBSERVATIONS  : {data}")
        data = {"average_distance": data["average_distance"],
                "heading": data["heading"],
                "date": data["date"]}
        return data


class Observation_L(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    latitude = fields.Int()
    longitude = fields.Int()
    nr_of_sightings = fields.Int()
    average_distance = fields.Int()
    heading = fields.Int()

    @pre_load
    def serialize_metadata(self, data, **kwargs):
        return data