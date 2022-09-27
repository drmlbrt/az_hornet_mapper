# instance/config.py
# http://exploreflask.com/en/latest/configuration.html
# __file__ --> basic.py where is it in my computer - where do I start and it gives me the full directory path
# the os library saves you to grab that absolute path c://user/bart/something/scripts/program

import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables
# environment variables are accessible with the load

# basedir = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

SECRET_KEY = os.getenv("API_KEY")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(PROJECT_ROOT, "hornets.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_SORT_KEYS = False


RAW_URI = True
REQUEST_URI = True

# MINOR ENVIRONMENT BASED CONFIG
DEBUG = True

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True