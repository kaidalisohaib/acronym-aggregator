from datetime import datetime
from pathlib import Path

import sqlalchemy as sa
from app import db, ma
from marshmallow import ValidationError
from marshmallow_jsonapi import Schema, fields
from sqlalchemy import UniqueConstraint


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
    created_by = db.Column(db.String(), nullable=False)
    last_modified_by = db.Column(db.String(), nullable=True)
    __table_args__ = (
        UniqueConstraint(
            "acronym", "meaning", "comment", "company", name="acronym_info_uc"
        ),
    )

    def __init__(self, acronym, meaning, comment, company, user_email) -> None:
        super().__init__()
        self.acronym = acronym
        self.meaning = meaning
        self.comment = comment
        self.company = company
        self.created_by = user_email

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


def string_not_empty(value):
    if len(value.strip()) < 1:
        raise ValidationError("Field is empty or filled with spaces.")


class AcronymSchema(Schema):
    class Meta:
        type_ = "acronyms"
        model = Acronym
        strict = True

    id = fields.Int(dump_only=True)
    acronym = fields.Str(required=True, validate=string_not_empty)
    meaning = fields.Str(required=True, validate=string_not_empty)
    comment = fields.Str(allow_none=True)
    company = fields.Str(required=True, validate=string_not_empty)
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
    zip_path = fields.Str(required=True, validate=string_not_empty)
