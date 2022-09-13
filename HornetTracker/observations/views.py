import copy
import os
from flask import Flask, render_template, url_for, redirect, Blueprint, flash, request, Response, jsonify
import time
from marshmallow import ValidationError
from HornetTracker.observations.models.observation import Observation
from HornetTracker.observations.schemas.s_observation import Observation_D, Observation_L
from HornetTracker.observations.forms.f_observations import AddObservation
from HornetTracker.modules.workers import longlatformatter
from HornetTracker.hornets.models.hornet import Hornet

observation_bp = Blueprint('observation', __name__,
                           url_prefix='/observation/',
                           template_folder="templates")

schema_observation_dump = Observation_D()
schema_observation_load = Observation_L()


@observation_bp.route("/get_all", methods=["GET", "POST"])
def get_all_observation_locations():
    all_observations = Observation.query.all()
    results = []
    for item in all_observations:
        try:
            result = schema_observation_dump.dump(item)
            results.append(result)

        except ValidationError as err:
            return {"message": err.messages}, 422

    return {"observations_data": results}


@observation_bp.route("/add", methods=["POST"])
def add_observation_locations():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No Valid JSON input data provided"}, 400
    for item in json_data["add_new_observation"]:
        print(item)
        Observation(**item).create()
    return {"message": "data uploaded"}


@observation_bp.route("/forms", methods=["GET", "POST"])
def observation_forms():
    form1 = AddObservation()

    if form1.submit1.data and form1.validate_on_submit():

        goodlat = longlatformatter(form1.latitude.data)

        goodlong = longlatformatter(form1.longitude.data)

        new_observation = {"latitude": goodlat,
                           "longitude": goodlong,
                           "average_distance": form1.average_distance.data,
                           "heading": form1.heading.data}

        try:
            new_observation = Observation(**new_observation).create()
            new_observation.bind_to_jar(**{"observation_id": new_observation._id ,
            "jar_id": form1.jar_name.data._id})   # this is an object returned from the select field in the form.

            flash(f"Added {form1.jar_name.data.jar_name} information to db", "success")
            redirect(url_for(".observation_forms"))

        except Exception:
            flash(f"{form1.jar_name.data.jar_name} encountered an issue", "danger")
            redirect(url_for(".observation_forms"))

    #     add the observation to the selected jar





    else:
        print(form1.errors)

    return render_template("/observations/add_observation.html",
                           addform=form1)


@observation_bp.route("/get_geo_data/<jar>", methods=["GET", "POST"])
def get_geodata(jar):
    """Takes in a string - the jar name must be the 'id' of the jar
    This function is used to pre-fill in the form data with a javascript
    """

    print(type(jar))

    print(jar.isnumeric())
    if jar.isnumeric() is True:
        jar = Hornet.find_by_db_id(jar)
    else:
        jar = Hornet.find_one_by_name(jar)

    if jar:
        lat = jar.latitude
        long = jar.longitude
        jarobj = {}
        jarobj["latitude"] = lat
        jarobj["longitude"] = long

    return jsonify({"jars": jarobj})


@observation_bp.route("/table", methods=["GET", "POST"])
def table_observations():
    all_observations = Observation.list()

    return render_template("/observations/table.html",
                           observations=all_observations)
