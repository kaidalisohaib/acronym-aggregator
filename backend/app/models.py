from datetime import datetime
from pathlib import Path

from app import db
from marshmallow import ValidationError
from marshmallow_jsonapi import Schema, fields
from sqlalchemy import UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


class Acronym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(), nullable=False)
    meaning = db.Column(db.String(), nullable=False)
    comment = db.Column(db.String(), nullable=True)
    company = db.Column(db.String(), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    last_modified_at = db.Column(
        db.DateTime(timezone=True), onupdate=datetime.utcnow, nullable=True
    )
    created_by = db.Column(db.String(), db.ForeignKey(User.email), nullable=False)
    last_modified_by = db.Column(db.String(), db.ForeignKey(User.email), nullable=True)

    created_user = db.relationship(User, foreign_keys=[created_by])
    modified_user = db.relationship(User, foreign_keys=[last_modified_by])

    __table_args__ = (
        UniqueConstraint(
            "acronym", "meaning", "comment", "company", name="acronym_info_uc"
        ),
    )

    def __init__(self, acronym, meaning, comment, company, user: User) -> None:
        super().__init__()
        self.acronym = acronym
        self.meaning = meaning
        self.comment = comment
        self.company = company
        self.created_by = user.email

    def set_modified_user(self, user: User):
        self.last_modified_by = user.email

    def __repr__(self) -> str:
        return "<Acronym id: {} acronym: {}>".format(self.id, self.acronym)


class Report(db.Model):
    """Report table for versioning

    The id represent the version, starting from 1.
    """

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    zip_path = db.Column(db.String, nullable=False)

    def __init__(self, zip_path: Path) -> None:
        super().__init__()
        self.zip_path = str(zip_path.absolute())

    def __repr__(self) -> str:
        return "<Report id: {} zip_path: {}>".format(self.id, self.zip_path)


def string_not_empty_validator(value):
    if len(value.strip()) < 1:
        raise ValidationError("Field is empty or filled with spaces.")


class AcronymSchema(Schema):
    class Meta:
        type_ = "acronyms"
        model = Acronym
        strict = True

    id = fields.Int(dump_only=True)
    acronym = fields.Str(required=True, validate=string_not_empty_validator)
    meaning = fields.Str(required=True, validate=string_not_empty_validator)
    comment = fields.Str(allow_none=True)
    company = fields.Str(required=True, validate=string_not_empty_validator)
    created_at = fields.DateTime(allow_none=True)
    last_modified_at = fields.DateTime(allow_none=True)
    created_by = fields.Email(allow_none=True)
    last_modified_by = fields.Email(allow_none=True)


class ReportSchema(Schema):
    class Meta:
        type_ = "reports"
        model = Acronym
        strict = True

    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(allow_none=True)
    zip_path = fields.Str(required=True, validate=string_not_empty_validator)
