from config import Config
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db: SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
ma: Marshmallow = Marshmallow(app)

from app import models, routes


def init_db():
    db.create_all()
    db.session.commit()
