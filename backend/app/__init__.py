from http.client import UNAUTHORIZED

from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api, abort
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)
# Choosing which config class to load
if Config.FLASK_ENV == "development":
    app.config.from_object(DevelopmentConfig)
elif Config.FLASK_ENV == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(TestingConfig)

db: SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

# Import the models so the db can create the tables
from app import models

db.create_all()
db.session.commit()

from app.models import User
from app.ressources import errors


# Setting up jwt identity loader so that JWTManager can get the current user
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Setting up jwt lookup loader so that JWTManager can get the id of the user
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = User.query.get(identity)
    if not user:
        abort(
            UNAUTHORIZED,
            errors=[{"status": UNAUTHORIZED, "detail": "User doesn't exist."}],
        )
    return user


# Add all the resource and route
from app.ressources.acronym import AcronymResource
from app.ressources.acronyms import AcronymsListResource
from app.ressources.login_register import LoginResource, RegisterResource
from app.ressources.report import ReportResource
from app.ressources.reports import ReportsListResource
from app.ressources.upload_csv import UploadCSVResource

api.add_resource(AcronymResource, "/api/acronyms/<int:acronym_id>")
api.add_resource(AcronymsListResource, "/api/acronyms")

api.add_resource(ReportResource, "/api/reports/<int:version>")
api.add_resource(ReportsListResource, "/api/reports")

api.add_resource(UploadCSVResource, "/api/upload")

api.add_resource(RegisterResource, "/api/register")
api.add_resource(LoginResource, "/api/login")
