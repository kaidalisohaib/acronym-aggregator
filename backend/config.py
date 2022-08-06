import os
import tempfile
from datetime import timedelta

from environs import Env

# basedir = os.path.abspath(os.path.dirname(__file__))

env = Env()
env.read_env()


class Config(object):
    SECRET_KEY = env.str("SECRET_KEY", "this-needs-to-be-changed!")
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    TMP_FOLDER = env.path("TMP_FOLDER", tempfile.gettempdir())
    REPORTS_FOLDER = env.path("REPORTS_FOLDER")
    UPLOAD_FOLDER = env.path("UPLOAD_FOLDER")
    ALLOWED_EXTENSIONS = env.path("ALLOWED_EXTENSIONS")
    JWT_SECRET_KEY = env("JWT_SECRET_KEY", "this-needs-to-be-changed!")
    JWT_ACCESS_TOKEN_EXPIRES = env.timedelta(
        "JWT_ACCESS_TOKEN_EXPIRES", timedelta(days=1)
    )
