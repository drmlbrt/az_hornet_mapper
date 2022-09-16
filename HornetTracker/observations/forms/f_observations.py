from flask_wtf import FlaskForm
from wtforms import (SelectField, SubmitField, StringField,
                     BooleanField, DateTimeField, RadioField,
                     TextAreaField, IntegerField, ValidationError, EmailField, validators, FloatField, HiddenField)
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from HornetTracker.jars.models.jar import Jar
from HornetTracker.modules.workers import longlatformatter


class AddObservation(FlaskForm):
    jar_name = QuerySelectField(get_label="jar_name",
                                query_factory=lambda: Jar.list(),
                                allow_blank=True,
                                validators=[validators.DataRequired()]
                                )
    longitude = StringField("Longitude", [InputRequired()])
    latitude = StringField("Latitude", [InputRequired()])
    average_distance = IntegerField("Average Distance", [InputRequired()])
    heading = IntegerField("Heading", [InputRequired()])
    submit1 = SubmitField("Add Observation", [InputRequired()])

