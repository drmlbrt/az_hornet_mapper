from flask_wtf import FlaskForm
from wtforms import (SelectField, SubmitField, StringField,
                     BooleanField, DateTimeField, RadioField,
                     TextAreaField, IntegerField, ValidationError, EmailField, validators, FloatField)
from wtforms.validators import InputRequired, Length, DataRequired
from HornetTracker.map.models.map import Map


class AddMapForm(FlaskForm):
    map_name = StringField("Map name", [validators.DataRequired(), validators.Length(min=3, max=8)])
    longitude = FloatField("Longitude")
    latitude = FloatField("Latitude")
    submit = SubmitField("Add Map")


class ShowMap(FlaskForm):
    map_name = SelectField("Map Name",
                           choices=[map.map_name for map in Map.query.all()])
    submit = SubmitField("Show Map Data")


class DeleteMap(FlaskForm):
    map_name = SelectField("Map Name",
                           choices=[map.map_name for map in Map.query.all()])
    submit = SubmitField("Delete Map Data")


class GenerateMap(FlaskForm):
    map_name = SelectField("Map Name",
                           choices=[map.map_name for map in Map.query.all()])
    submit = SubmitField("Generate Map Data")


class UpdateMap(FlaskForm):
    map_name = StringField("Map name", [validators.DataRequired(), validators.Length(min=3, max=25)])
    longitude = FloatField("Longitude")
    latitude = FloatField("Latitude")
    submit = SubmitField("Update Map Data")
