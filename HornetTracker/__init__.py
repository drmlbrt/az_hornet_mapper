import json

from flask import Flask, render_template, flash, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_statistics import Statistics
from HornetTracker.modules.csrf import csrf, CSRFError
from werkzeug.exceptions import HTTPException, BadRequest
from flask_debugtoolbar import DebugToolbarExtension
from logging.config import dictConfig
import os
import logging
from flask import has_request_context, request
from flask.logging import default_handler

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)
static = os.path.join(
    package_dir, "static"
)

app = Flask(__name__, instance_relative_config=True)
app.debug = False
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.static_folder = static
# removing the default handler
app.logger.removeHandler(default_handler)

db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)


##### STATISTICS COLLECTOR
class Request(db.Model):
    __tablename__ = "request"

    index = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
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

from HornetTracker.jars.models.jar import Jar
from HornetTracker.map.models.map import Map
from HornetTracker.observations.models.observation import Observation

from HornetTracker.jars.routes import hornet_bp as hornet_blueprint
from HornetTracker.map.routes import map_bp as map_blueprint
from HornetTracker.observations.routes import observation_bp as observation_blueprint

app.register_blueprint(hornet_blueprint)
app.register_blueprint(map_blueprint)
app.register_blueprint(observation_blueprint)

# SECURITY
# Have cookie sent
app.config["SECURITY_CSRF_COOKIE_NAME"] = "XSRF-TOKEN"

# Don't have csrf tokens expire (they are invalid after logout)
app.config["WTF_CSRF_TIME_LIMIT"] = None

# You can't get the cookie until you are logged in.
app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True

# JINJA protection
app.jinja_options["autoescape"] = lambda _: True

csrf.init_app(app)


@app.errorhandler(CSRFError)
def handle_csrf_error():
    flash("There is a csrf token issue")
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400


@app.route('/', methods=["GET"])
def index():
    make_response(), {"Access-Control-Allow-Origin": "*"}
    make_response(), {"Strict-Transport-Security": "max-age=31536000; includeSubDomains"}
    make_response(), {'Content-Security-Policy': "default-src 'self'"}

    return render_template("index.html")

# @app.route('/.well-known/host-meta', methods=["GET"])
# def well_known_host_meta():
#     return render_template("well_known_host_meta.html")
