from datetime import datetime

from app import db


class Acronym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(), nullable=False)
    meaning = db.Column(db.String(), nullable=False)
    comment = db.Column(db.String(), nullable=True)
    company = db.Column(db.String(), nullable=False)
    created_when = db.Column(db.DateTime, default=datetime.utcnow())
    last_modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    created_by = db.Column(db.String(), nullable=False)
    last_modified_by = db.Column(db.String(), nullable=False)

    def __init__(self, acronym, meaning, comment, company, user_email) -> None:
        super().__init__()
        self.acronym = acronym
        self.meaning = meaning
        self.comment = comment
        self.company = company
        self.created_by = user_email
        self.last_modified_by = user_email

    def __repr__(self) -> str:
        return "<Acronym id:{} acronym:{}>".format(self.id, self.acronym)
