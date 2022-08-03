import json

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import datetime

import os

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)
static = os.path.join(
    package_dir, "static"
)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.static_folder = static

db = SQLAlchemy(app)

# db.create_all()
# db.session.commit()

from HornetTracker.hornets.models.hornet import Hornet
from HornetTracker.map.models.map import Map

from HornetTracker.hornets.views import hornet_bp as hornet_blueprint
from HornetTracker.map.views import map_bp as map_blueprint

app.register_blueprint(hornet_blueprint)
app.register_blueprint(map_blueprint)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/.well-known/host-meta', methods=["GET"])
def well_known_host_meta():
    return render_template("well_known_host_meta.html")
