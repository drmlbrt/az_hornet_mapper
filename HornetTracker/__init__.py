import json

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_statistics import Statistics
from flask_wtf.csrf import CSRFProtect

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


##### STATISTICS COLLECTOR
class Request(db.Model):
    __tablename__ = "request"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_time = db.Column(db.Float)
    date = db.Column(db.DateTime)
    method = db.Column(db.String)
    size = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    path = db.Column(db.String)
    user_agent = db.Column(db.String)
    remote_address = db.Column(db.String)
    exception = db.Column(db.String)
    referrer = db.Column(db.String)
    browser = db.Column(db.String)
    platform = db.Column(db.String)
    mimetype = db.Column(db.String)


statistics = Statistics(app, db, Request)
##########################


with app.app_context():
    db.create_all()

from HornetTracker.hornets.models.hornet import Hornet
from HornetTracker.map.models.map import Map

from HornetTracker.hornets.views import hornet_bp as hornet_blueprint
from HornetTracker.map.views import map_bp as map_blueprint

app.register_blueprint(hornet_blueprint)
app.register_blueprint(map_blueprint)

# SECURITY
app.jinja_options["autoescape"] = lambda _: True
csrf = CSRFProtect(app)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

# @app.route('/.well-known/host-meta', methods=["GET"])
# def well_known_host_meta():
#     return render_template("well_known_host_meta.html")
