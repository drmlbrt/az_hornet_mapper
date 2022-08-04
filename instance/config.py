# instance/config.py
# http://exploreflask.com/en/latest/configuration.html
# __file__ --> basic.py where is it in my computer - where do I start and it gives me the full directory path
# the os library saves you to grab that absolute path c://user/bart/something/scripts/program

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "thisisasecretkey"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "hornets.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False


RAW_URI = True
REQUEST_URI = True

# MINOR ENVIRONMENT BASED CONFIG
DEBUG = True