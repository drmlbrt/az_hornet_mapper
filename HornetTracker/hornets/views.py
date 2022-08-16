import copy
import os
from flask import Flask, render_template, url_for, redirect, Blueprint, flash, request
import folium
from folium import plugins
from marshmallow import ValidationError
from HornetTracker.hornets.models.hornet import Hornet
from HornetTracker.map.models.map import Map
from HornetTracker.hornets.schemas.s_hornet import Hornet_D, Hornet_L
from HornetTracker.hornets.forms.f_hornet import AddJar, UpdateJar, ShowJar, BindMapToJar, DeleteJar, CsvReadData, \
    DeleteButtonJar
from HornetTracker.generator.csv_reader import csv_reader

hornet_bp = Blueprint('hornet', __name__,
                      url_prefix='/hornet/',
                      template_folder="templates")

schema_hornet_dump = Hornet_D()
schema_hornet_load = Hornet_L()


@hornet_bp.route("/get_all", methods=["GET", "POST"])
def get_all_hornet_locations():
    all_hornets = Hornet.query.all()
    results = []
    for item in all_hornets:
        try:
            result = schema_hornet_dump.dump(item)
            results.append(result)

        except ValidationError as err:
            return {"message": err.messages}, 422

    return {"hornets_data": results}


@hornet_bp.route("/add", methods=["POST"])
def add_hornet_locations():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No Valid JSON input data provided"}, 400

    for item in json_data["add_new_hornet_site"]:
        print(item)

        Hornet(**item).create()

    return {"message": "data uploaded"}


@hornet_bp.route("/update", methods=["PATCH"])
def upate_hornet_locations():
    json_data = request.get_json()

    results = []

    if not json_data:
        return {"message": "No Valid JSON input data provided"}, 400

    for item in json_data["update_hornets_data"]:
        jar = Hornet.find_one_by_name(jar_name=item["jar_name"])

        if jar:
            update = Hornet.update(jar=item)
            if update:
                results.append(f"Update for item {item['jar_name']} OK")
            else:
                results.append(f"Update for item {item['jar_name']} FAILED")
        else:
            return {"message": "Something went wrong with the update"}, 400

    return {"Update_Results": results}, 200


@hornet_bp.route("/delete", methods=["DELETE"])
def jar_delete():
    json_data = request.get_json()

    results = []

    if not json_data:
        return {"message": "No Valid JSON input data provided"}, 400

    for item in json_data["delete_jar_data"]:

        jar = Hornet.find_one_by_name(jar_name=item["jar_name"])

        if jar:
            update = Hornet.delete(jar)
            if update:
                results.append(f"Delete for item {item['jar_name']} OK")
            else:
                results.append(f"Delete for item {item['jar_name']} FAILED - Does it exist?")
        else:
            return {"message": "Something went wrong with the update"}, 400

    return {"delete_results": results}, 200


@hornet_bp.route("/add_jar_to_map", methods=["PATCH"])
def add_jar_to_map():
    json_data = request.get_json()

    results = []

    if not json_data:
        return {"message": "No Valid JSON input data provided"}, 400

    for item in json_data["bind_jar_to_map"]:

        jar = Hornet.find_one_by_name(jar_name=item["jar_name"])

        if jar:
            update = Hornet.bind_to_map(bind_jar_to_map=item)
            if update:
                results.append(f"Update for item {item['jar_name']} OK")
        else:
            results.append(f"Update for item {item['jar_name']} FAILED - there is none "), 400

    return {"Update_Results": results}, 200


@hornet_bp.route("/forms", methods=["GET", "POST"])
def hornet_forms():
    form1 = AddJar()
    form2 = UpdateJar()
    form3 = ShowJar()
    form4 = BindMapToJar()
    form5 = DeleteJar()

    if form1.submit1.data and form1.validate_on_submit():
        new_jar = {"jar_name": form1.jar_name.data,
                   "latitude": form1.latitude.data,
                   "longitude": form1.longitude.data,
                   "nr_of_sightings": form1.nr_of_sightings.data,
                   "average_distance": form1.average_distance.data,
                   "heading": form1.heading.data}

        Hornet(**new_jar).create()

        flash(f"Added {new_jar['jar_name']} information to db")

        redirect(url_for(".hornet_forms"))

    if form3.submit2.data and form3.validate_on_submit():
        selected_jar = form3.jar_name.data

        _jar = Hornet.find_one_by_name(jar_name=selected_jar.__dict__["jar_name"])

        print(f"----------------------- {_jar}")

        form2 = UpdateJar()
        form2.jar_name.data = _jar.jar_name
        form2.latitude.data = _jar.latitude
        form2.longitude.data = _jar.longitude
        form2.nr_of_sightings.data = _jar.nr_of_sightings
        form2.average_distance.data = _jar.average_distance
        form2.heading.data = _jar.heading

        print(f"----------------------- {form2.data}")

        redirect(url_for(".hornet_forms"))

    if form2.update.data and form2.validate_on_submit():

        update_jar = {"jar_name": form2.jar_name.data,
                      "latitude": form2.latitude.data,
                      "longitude": form2.longitude.data,
                      "nr_of_sightings": form2.nr_of_sightings.data,
                      "average_distance": form2.average_distance.data,
                      "heading": form2.heading.data}

        print(f"----------------------- {update_jar}")



        jar = Hornet.find_one_by_name(jar_name=update_jar["jar_name"])

        print(f"----------------------- {jar}")

        try:

            if jar:
                jar.update(jar=update_jar)

                flash(f"Updated {update_jar['jar_name']}")
        except Exception:
            print(f"----------------------- {Exception}")
            flash("Something went wrong with the update.")

        redirect(url_for(".hornet_forms"))

    if form4.submit4.data and form4.validate_on_submit():
        jar_name = form4.jar_name.data
        map_name = form4.map_name.data

        binding = {"jar_name": jar_name.__dict__["jar_name"],
                   "map_name": map_name.__dict__["map_name"]}

        jar = Hornet.find_one_by_name(jar_name=binding["jar_name"])

        if jar:
            Hornet.bind_to_map(bind_jar_to_map=binding)

        flash(f"Map '{binding['map_name']}' and Jar '{binding['jar_name']}' are related")

        redirect(url_for(".hornet_forms"))

    if form5.submit5.data and form5.validate_on_submit():
        selected_jar = form5.jar_name.data
        jar = Hornet.find_one_by_name(jar_name=selected_jar.__dict__["jar_name"])
        if jar:
            delete = Hornet.delete(jar)
            if delete:
                flash(f"Delete for item {selected_jar.__dict__['jar_name']} OK")
            else:
                flash(f"Delete for item {selected_jar.__dict__['jar_name']} FAILED - Does it exist?")
        else:
            flash("Something went wrong with the update"), 400

        redirect(url_for(".hornet_forms"))

    return render_template("/hornets/add_jar.html",
                           addform=form1,
                           updateform=form2,
                           showjar=form3,
                           binder=form4,
                           delete=form5)


@hornet_bp.route("/table", methods=["GET", "POST"])
def table_jars():
    all_jars = Hornet.query.all()
    all_maps = Map.query.all()
    binder = BindMapToJar()

    return render_template("/hornets/table.html",
                           jars=all_jars, binder=binder, maps=all_maps)


@hornet_bp.route("/delete_jar_name=<string:jar_name>", methods=["DELETE", "POST", "GET"])
def _jar_name_delete(jar_name):
    jar = Hornet.find_one_by_name(jar_name=jar_name)
    if jar:
        update = Hornet.delete(jar)
        if update:
            flash(f"Delete for item {jar_name} OK")
        else:
            flash(f"Delete for item {jar_name} FAILED - Does it exist?")

        return redirect(url_for(".table_jars"))
    else:
        return {"message": "Something went wrong with the update"}, 400


@hornet_bp.route("/add_jar_on_map", methods=["POST", "GET"])
def _jar_on_map():
    returneddata = {}

    print(request.args)

    returneddata["jar_name"] = request.args.get('jar_name')
    returneddata["map_name"] = request.args.get('map_name')

    print(f"-------------------{returneddata['jar_name']}")

    print(f"-------------------{returneddata['map_name']}")

    jar = Hornet.find_one_by_name(jar_name=returneddata["jar_name"])

    if jar:
        update = Hornet.bind_to_map(bind_jar_to_map=returneddata)
        if update:
            flash(f"Adding Map {returneddata['map_name']} for item {returneddata['jar_name']} OK")
        else:
            flash(f"Adding Map {returneddata['map_name']} for item {returneddata['jar_name']} FAILED - Does it exist?")

        return redirect(url_for(".table_jars"))

    flash("Something went wrong")
    return redirect(url_for(".table_jars"))


@hornet_bp.route("/csv_uploader", methods=["GET", "POST"])
def csv_upload():
    csv_form = CsvReadData()

    if csv_form.submit_csv_data.data and csv_form.validate_on_submit():

        csv_data = csv_reader(data=csv_form.csv_text.data)

        if csv_data:
            if isinstance(csv_data, list):
                for item in csv_data:
                    try:
                        Hornet(**item).create()
                    except TypeError as err:
                        flash(f"Error with data keyword : {err}")
            flash("Upload of data has finished")
        if csv_data is False:
            flash("The CSV data can't be processed")

        return redirect(url_for(".table_jars"))

    return render_template("/hornets/csv_uploader.html", csv_form=csv_form)
