from flask_wtf import FlaskForm
from wtforms import (SelectField, SubmitField, StringField,
                     BooleanField, DateTimeField, RadioField,
                     TextAreaField, IntegerField, ValidationError, EmailField, validators, FloatField, HiddenField)
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from HornetTracker.hornets.models.hornet import Hornet
from HornetTracker.modules.workers import longlatformatter


class AddObservation(FlaskForm):
    jar_name = QuerySelectField(get_label="jar_name",
                                query_factory=lambda: Hornet.list(),
                                allow_blank=True,
                                validators=[validators.DataRequired()]
                                )
    longitude = StringField("Longitude", [InputRequired()])
    latitude = StringField("Latitude", [InputRequired()])
    average_distance = StringField("Average Distance", [InputRequired()])
    heading = StringField("Heading", [InputRequired()])
    submit1 = SubmitField("Add Observation", [InputRequired()])

