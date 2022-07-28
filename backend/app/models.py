from datetime import datetime

from app import db, ma
from marshmallow_jsonapi import Schema, fields


class Acronym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(), nullable=False)
    meaning = db.Column(db.String(), nullable=False)
    comment = db.Column(db.String(), nullable=True)
    company = db.Column(db.String(), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow(), nullable=False
    )
    last_modified_at = db.Column(
        db.DateTime(timezone=True), onupdate=datetime.utcnow(), nullable=True
    )
    created_by = db.Column(db.String(), nullable=False)
    last_modified_by = db.Column(db.String(), nullable=True)

    def __init__(self, acronym, meaning, comment, company, user_email) -> None:
        super().__init__()
        self.acronym = acronym
        self.meaning = meaning
        self.comment = comment
        self.company = company
        self.created_by = user_email

    def __repr__(self) -> str:
        return "<Acronym id: {} acronym: {}>".format(self.id, self.acronym)


class AcronymSchema(Schema):
    class Meta:
        type_ = "acronyms"
        model = Acronym
        strict = True

    id = fields.Int(dump_only=True)
    acronym = fields.Str()
    meaning = fields.Str()
    comment = fields.Str()
    company = fields.Str()
    created_at = fields.DateTime()
    last_modified_at = fields.DateTime()
    created_by = fields.Email()
    last_modified_by = fields.Email()
