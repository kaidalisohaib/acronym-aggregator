import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this-needs-to-be-changed!"
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"] or False
    )
    TMP_FOLDER = os.environ.get("TMP_FOLDER")
    REPORTS_FOLDER = os.environ.get("REPORTS_FOLDER")
    ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
