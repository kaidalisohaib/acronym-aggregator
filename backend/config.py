import os
import tempfile
from datetime import timedelta

from environs import Env

env = Env()
env.read_env()


def create_db_url(user, pw, url, db):
    return f"postgresql://{user}:{pw}@{url}/{db}"


def get_env_db_url(env_setting):
    if env_setting == "development":
        POSTGRES_USER = env.str("DEV_POSTGRES_USER")
        POSTGRES_PW = env.str("DEV_POSTGRES_PW")
        POSTGRES_URL = env.str("DEV_POSTGRES_URL")
        POSTGRES_DB = env.str("DEV_POSTGRES_DB")
    elif env_setting == "testing":
        POSTGRES_USER = env.str("TESTING_POSTGRES_USER")
        POSTGRES_PW = env.str("TESTING_POSTGRES_PW")
        POSTGRES_URL = env.str("TESTING_POSTGRES_URL")
        POSTGRES_DB = env.str("TESTING_POSTGRES_DB")
    elif env_setting == "production":
        POSTGRES_USER = env.str("PROD_POSTGRES_USER")
        POSTGRES_PW = env.str("PROD_POSTGRES_PW")
        POSTGRES_URL = env.str("PROD_POSTGRES_URL")
        POSTGRES_DB = env.str("PROD_POSTGRES_DB")

    return create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)


# DB URLS for each Environment
DEV_DB_URL = get_env_db_url("development")
TESTING_DB_URL = get_env_db_url("testing")
PROD_DB_URL = get_env_db_url("production")


class Config(object):
    FLASK_ENV = env.str("FLASK_ENV", "development")
    FLASK_SECRET_KEY = env.str("SECRET_KEY", "this-needs-to-be-changed!")
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    TMP_FOLDER = env.path("TMP_FOLDER", tempfile.gettempdir())
    REPORTS_FOLDER = env.path("REPORTS_FOLDER")
    UPLOAD_FOLDER = env.path("UPLOAD_FOLDER")
    ALLOWED_EXTENSIONS = env.list("ALLOWED_EXTENSIONS")
    JWT_SECRET_KEY = env("JWT_SECRET_KEY", "this-needs-to-be-changed!")
    JWT_ACCESS_TOKEN_EXPIRES = env.timedelta(
        "JWT_ACCESS_TOKEN_EXPIRES", timedelta(days=1)
    )
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    pass


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = TESTING_DB_URL
    DEBUG = True
    TESTING = True
    pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = PROD_DB_URL
    pass
