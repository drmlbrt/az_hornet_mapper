from flask_wtf import FlaskForm
from wtforms import (SelectField, SubmitField, StringField,
                     BooleanField, DateTimeField, RadioField,
                     TextAreaField, IntegerField, ValidationError, EmailField, validators, FloatField, HiddenField)
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from HornetTracker.hornets.models.hornet import Hornet
from HornetTracker.map.models.map import Map
from HornetTracker.modules.workers import longlatformatter


class AddJar(FlaskForm):
    jar_name = StringField("Jar Name", [validators.DataRequired(), validators.Length(min=3, max=60)])
    longitude = StringField("Longitude", [InputRequired()])
    latitude = StringField("Latitude", [InputRequired()])
    nr_of_sightings = StringField("Nr Of Sightings", [InputRequired()])
    average_distance = StringField("Average Distance", [InputRequired()])
    heading = StringField("Heading", [InputRequired()])

    submit1 = SubmitField("Add Jar", [InputRequired()])



class ShowJar(FlaskForm):
    jar_name = QuerySelectField(get_label="jar_name",
                                query_factory=lambda: Hornet.list())

    submit2 = SubmitField("Show Jar Data")


class UpdateJar(FlaskForm):
    jar_name = StringField("Jar Name")
    longitude = FloatField("Longitude - dot notation!")
    latitude = FloatField("Latitude - dot notation!")
    nr_of_sightings = StringField('Nr Of Sightings', [InputRequired()])
    average_distance = StringField('Average Distance', [InputRequired()])
    heading = StringField('Heading', [InputRequired()])

    update = SubmitField("Update Jar Data")




class BindMapToJar(FlaskForm):
    jar_name = QuerySelectField(get_label="jar_name",
                                query_factory=lambda: Hornet.list())
    map_name = QuerySelectField(get_label="map_name",
                                query_factory=lambda: Map.list())

    submit4 = SubmitField("Bind Jar To Map")


class DeleteJar(FlaskForm):
    jar_name = QuerySelectField(get_label="jar_name",
                                query_factory=lambda: Hornet.list())

    submit5 = SubmitField("Delete Jar Data")


class DeleteButtonJar(FlaskForm):
    delete_name = HiddenField("Hidden Table Name")
    delete = SubmitField('Delete')


class CsvReadData(FlaskForm):
    csv_text = TextAreaField()
    submit_csv_data = SubmitField("Submit CSV")
