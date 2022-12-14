from flask import Flask, render_template, url_for, redirect, Blueprint, request, flash, Response
from marshmallow import ValidationError
from HornetTracker.map.models.map import Map
from HornetTracker.map.schemas.s_map import Map_D, Map_L
from HornetTracker.map.forms.f_map import AddMapForm, UpdateMap, ShowMap, GenerateMap, DeleteMap, FindMap
from HornetTracker.modules.map_generator import generate_map, base_map
from HornetTracker.modules.api_map_finder import mapfinder
from HornetTracker.modules.workers import longlatformatter

map_bp = Blueprint('map', __name__,
                   url_prefix='/map',
                   template_folder="templates")

schema_hornet_dump = Map_D()
schema_hornet_load = Map_L()

base_map = base_map()


@map_bp.route("/get_all", methods=["GET", "POST"])
def get_all_maps():
    all_hornets = Map.list()
    results = []
    for item in all_hornets:
        try:
            result = schema_hornet_dump.dump(item)
            results.append(result)

        except ValidationError as err:
            return {"message": err.messages}, 422

    return {"maps_data": results}


@map_bp.route("/add", methods=["POST"])
def add_map():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No Valid JSON input data provided"}, 400

    for item in json_data["add_new_hornet_site"]:
        print(item)

        Map(**item).create()

    return {"message": "data uploaded"}


@map_bp.route("/update", methods=["PATCH"])
def update_map_locations():
    json_data = request.get_json()

    results = []

    if not json_data:
        return {"message": "No Valid JSON input data provided"}, 400

    for item in json_data["update_maps_data"]:
        jar = Map.find_one_by_name(map_name=item["map_name"])

        if jar:
            update = Map.update(map=item)
            if update:
                results.append(f"Update for item {item['jar_name']} OK")
            else:
                results.append(f"Update for item {item['jar_name']} FAILED")
        else:
            return {"message": "Something went wrong with the update"}, 400

    return {"Update_Results": results}, 200


@map_bp.route("/delete", methods=["DELETE"])
def delete_map():
    json_data = request.get_json()
    results = []

    if not json_data:
        return {"message": "No Valid JSON input data provided"}, 400

    for item in json_data["delete_maps_data"]:
        jar = Map.find_one_by_name(map_name=item["map_name"])

        if jar:
            update = Map.delete(jar)
            if update:
                results.append(f"Delete for item {item['jar_name']} OK")
            else:
                results.append(f"Delete for item {item['jar_name']} FAILED")
        else:
            return {"message": "Something went wrong with the update"}, 400

    return {"delete_results": results}, 200


@map_bp.route("/forms", methods=["GET", "POST"])
def maps_forms():

    form1 = AddMapForm()
    form2 = UpdateMap()
    form3 = ShowMap()
    form5 = DeleteMap()
    finder = FindMap()

    if form1.submit1.data and form1.validate_on_submit():

        goodlat = longlatformatter(form1.latitude.data)
        goodlong = longlatformatter(form1.longitude.data)

        new_map = {"map_name": form1.map_name.data,
                   "latitude": goodlat,
                   "longitude": goodlong}

        _new_map =  Map(**new_map).create()

        if _new_map is True:
            flash(f"Added {new_map['map_name']} information to db", "success")
            redirect(url_for(".maps_forms"))
        else:
            flash(f"{new_map['map_name']} ALREAdY EXISTS", "danger")
            redirect(url_for(".maps_forms"))

    if form3.submit2.data and form3.validate_on_submit():
        selected_map = form3.map_name.data

        _jar = Map.find_one_by_name(map_name=selected_map.__dict__["map_name"])

        form2 = UpdateMap(obj=_jar)

        redirect(url_for(".maps_forms"))

    if form2.submit5.data and form2.validate_on_submit():

        update_map = {"map_name": form2.map_name.data,
                      "latitude": form2.latitude.data,
                      "longitude": form2.longitude.data}

        _map = Map.find_one_by_name(map_name=update_map["map_name"])

        if _map:
            _map.update(map=update_map)

        flash(f"Updated {update_map['map_name']}", "success")

        redirect(url_for(".maps_forms"))

    if form5.delete_map.data and form5.validate_on_submit():
        selected_map = form5.map_name.data
        _map = Map.find_one_by_name(map_name=selected_map.__dict__["map_name"])

        if _map:
            update = Map.delete(_map)
            if update:
                flash(f"Delete for item {selected_map.__dict__['map_name']} OK", "success")
            else:
                flash(f"Delete for item {selected_map.__dict__['map_name']} FAILED - Does it exist?", "danger")
        else:
            flash("Something went wrong with the update", "danger"), 400

        redirect(url_for(".maps_forms"))

    if finder.find.data and finder.validate_on_submit():
        address = finder.address.data

        find_address = mapfinder(address)
        print("****************************************BACK FROM THE FORM AND MAPFINDER")
        print(type(find_address))
        print(f"We have found : {find_address}")

        if isinstance(find_address, object): # the object should only be a flash message
            if find_address.__repr__() is None:
                print("this is an object, should be a flash message for flask")
                find_address
                return redirect(url_for(".maps_forms"))
            else:
                pass

        print(f"------------------------------------------FOUND ADDRESS-----{find_address}")

        if find_address is False:
            flash(f"No results for {str(find_address).upper()} input", "warning")
            return redirect(url_for(".maps_forms"))

        elif isinstance(find_address, list):
            print("=========================================================== Found a list of items")
            flash(f"{find_address}", "warning")
            return redirect(url_for(".maps_forms"))

        else:
            print("Arrived at the else after one address found!!!")
            if isinstance(find_address, dict):
                new_map = generate_map(map_data=find_address)

                return render_template("/map/add_map.html",
                           addform=form1,
                           updateform=form2,
                           showmap=form3,
                           delete=form5,
                           finder=finder,
                           map=new_map)

    return render_template("/map/add_map.html",
                           addform=form1,
                           updateform=form2,
                           showmap=form3,
                           delete=form5,
                           finder=finder,
                           map=base_map)


@map_bp.route("/generate_map", methods=["GET", "POST"])
def generate_new_map():
    generate_map_form = GenerateMap()
    if generate_map_form.submit4.data and generate_map_form.validate_on_submit():
        selected_map = generate_map_form.map_name.data
        map = Map.find_one_by_name(map_name=selected_map.__dict__["map_name"])
        new_map = map.generate_map(latitude=map.latitude,longitude=map.longitude)
        if len(map.jar_id) > 0:
            for jar in map.jar_id:
                Map.generate_map_marker(parent_map=new_map,
                                        jar=True,
                                        latitude=jar.latitude,
                                        longitude=jar.longitude)

                # find if there are any observations attached to that jar
                if jar.observation_id:
                    for observation in jar.observation_id:
                        Map.generate_map_marker(parent_map=new_map,
                                                observation=True,
                                                latitude=observation.latitude,
                                                longitude=observation.longitude,
                                                average_distance=observation.average_distance,
                                                heading=observation.heading)
        return render_template("/map/generate_map.html",
                               showmap=generate_map_form, map=new_map._repr_html_())
    return render_template("/map/generate_map.html",
                           showmap=generate_map_form)


@map_bp.route("/_generate_map/", methods=["GET", "POST"])
def _generate_new_map():
    returneddata = {}

    returneddata["map_name"] = request.args.get('map_name')

    map = Map.find_one_by_name(map_name=returneddata["map_name"])

    new_map = generate_map(map_data=map.__dict__)

    all_maps = Map.list()

    return render_template("/map/table.html",
                           maps=all_maps,
                           map=new_map)


@map_bp.route("/table", methods=["GET", "POST"])
def table_maps():
    all_maps = Map.list()
    return render_template("/map/table.html",
                           maps=all_maps,
                           )


@map_bp.route("/delete_map_name=<string:map_name>", methods=["DELETE", "POST", "GET"])
def _map_name_delete(map_name):
    jar = Map.find_one_by_name(map_name=map_name)

    if jar:
        update = Map.delete(jar)
        if update:
            flash(f"Delete for item {map_name} OK", "success")
        else:
            flash(f"Delete for item {map_name} FAILED - Does it exist?", "danger")

        return redirect(url_for(".table_maps"))

    else:
        return {"message": "Something went wrong with the update"}, 400
