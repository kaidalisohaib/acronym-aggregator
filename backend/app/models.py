from datetime import datetime
from pathlib import Path

from app import db
from marshmallow import ValidationError
from marshmallow_jsonapi import Schema, fields
from sqlalchemy import UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """
    # User table

    ## Columns:
    - id: Primary key.
    - email: Unique String, contains email of the user.
    - password_hash: String, contains hashed password of the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password: str) -> None:
        """Set the password_hash column to the hash of the password.

        Args:
            password (str): The password to set.
        """

        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the password is the correct user password.

        Args:
            password (str): Password to test.

        Returns:
            bool: True if it's correct, othersise False.
        """

        return check_password_hash(self.password_hash, password)


class Acronym(db.Model):
    """
    # Acronym table

    ## Columns:
    - id (int): Primary key.
    - acronym (str): Non-nullable, the acronym.
    - meaning (str): Non-nullable, the meaning of the acronym.
    - comment (str): Nullable, a comment about the acronym.
    - company (str): Non-nullable, the company the acronym belong to.
    - created_at (datetime): Non-nullable, When was the acronym created in UTC.
    - last_modified_at (datetime): Nullable, Last time the acronym was modified in UTC.
    - created_by (str): Non-nullable, The email of the user that created the acronym.
    - last_modified_by (str): Nullable, The email of the user that last
      modified the acronym.
    """

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

    # Two acronym can't have the same acronym, meaning,
    # comment and company at the same time
    __table_args__ = (
        UniqueConstraint(
            "acronym", "meaning", "comment", "company", name="acronym_info_uc"
        ),
    )

    def __init__(
        self, acronym: str, meaning: str, comment: str, company: str, user: User
    ) -> None:
        super().__init__()
        self.acronym = acronym
        self.meaning = meaning
        self.comment = comment
        self.company = company
        self.created_by = user.email

    def set_modified_user(self, user: User) -> None:
        """Change the last_modified_by to the user email.

        Args:
            user (User): The last user that changed the acronym.
        """
        self.last_modified_by = user.email

    def __repr__(self) -> str:
        return "<Acronym id: {} acronym: {}>".format(self.id, self.acronym)


class Report(db.Model):
    """# Report table

    ## Columns:
    - id (int): The id and version of the report.
    - created_at (datetime): When was the report created in UTC.
    - zip_path (str): The absolute path of the generate zip file.
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


def string_not_empty_validator(string: str):
    """Verify if a string is empty. Empty means that the length
    is zero or that the string contains only white space.

    Args:
        string (str): String to test.

    Raises:
        ValidationError: If the string is empty.
    """
    if len(string.strip()) < 1:
        raise ValidationError("Field is empty or filled with spaces.")


class AcronymSchema(Schema):
    """Acronym schema to dump an Acronym instance into json:api format."""

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
    """Report schema to dump a Report instance into json:api format."""

    class Meta:
        type_ = "reports"
        model = Acronym
        strict = True

    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(allow_none=True)
    zip_path = fields.Str(required=True, validate=string_not_empty_validator)
