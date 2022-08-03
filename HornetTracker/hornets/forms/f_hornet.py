from flask_wtf import FlaskForm
from wtforms import (SelectField, SubmitField, StringField,
                     BooleanField, DateTimeField, RadioField,
                     TextAreaField, IntegerField, ValidationError, EmailField, validators, FloatField)
from wtforms.validators import InputRequired, Length, DataRequired
from HornetTracker.hornets.models.hornet import Hornet
from HornetTracker.map.models.map import Map


class AddJar(FlaskForm):
    jar_name = StringField("Jar Name", [validators.DataRequired(), validators.Length(min=3, max=8)])
    longitude = FloatField("Longitude", [InputRequired()])
    latitude = FloatField("Latitude", [InputRequired()])
    nr_of_sightings = StringField("Nr Of Sightings", [InputRequired()])
    average_distance = StringField("Average Distance", [InputRequired()])
    heading = StringField("Heading", [InputRequired()])

    submit = SubmitField("Add Jar", [InputRequired()])


class ShowJar(FlaskForm):
    jar_name = SelectField("Jar Name",
                           choices=[jar.jar_name for jar in Hornet.query.all()])

    submit = SubmitField("Show Jar Data")


class UpdateJar(FlaskForm):
    jar_name = StringField("Jar Name")
    longitude = FloatField("Longitude")
    latitude = FloatField("Latitude")
    nr_of_sightings = StringField('Nr Of Sightings', [InputRequired()])
    average_distance = StringField('Average Distance', [InputRequired()])
    heading = StringField('Heading', [InputRequired()])

    submit = SubmitField("Update Jar Data")


class BindMapToJar(FlaskForm):
    jar_name = SelectField("Jar Name",
                           choices=[jar.jar_name for jar in Hornet.query.all()])
    map_name = SelectField("Map Name",
                           choices=[map.map_name for map in Map.query.all()])

    submit = SubmitField("Bind Jar To Map")
