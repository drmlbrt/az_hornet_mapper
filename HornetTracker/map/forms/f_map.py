from flask_wtf import FlaskForm
from wtforms import (SelectField, SubmitField, StringField,
                     BooleanField, DateTimeField, RadioField,
                     TextAreaField, IntegerField, ValidationError, EmailField, validators, FloatField)
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from HornetTracker.map.models.map import Map


class AddMapForm(FlaskForm):
    map_name = StringField("Map name", [validators.DataRequired(), validators.Length(min=3, max=25)])
    longitude = FloatField("Longitude")
    latitude = FloatField("Latitude")
    submit1 = SubmitField("Add Map")


class ShowMap(FlaskForm):
    map_name = QuerySelectField(get_label="map_name",
                                query_factory=lambda: Map.query.all())
    submit2 = SubmitField("Show Map Data")


class DeleteMap(FlaskForm):
    map_name = QuerySelectField(get_label="map_name",
                                query_factory=lambda: Map.query.all())
    submit3 = SubmitField("Delete Map Data")


class GenerateMap(FlaskForm):
    map_name = QuerySelectField(get_label="map_name",
                                query_factory=lambda: Map.query.all())
    submit4 = SubmitField("Generate Map Data")


class UpdateMap(FlaskForm):
    map_name = StringField("Map name", [validators.DataRequired(), validators.Length(min=3, max=25)])
    longitude = FloatField("Longitude")
    latitude = FloatField("Latitude")
    submit5 = SubmitField("Update Map Data")

