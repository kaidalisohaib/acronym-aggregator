from http.client import (
    CONFLICT,
    INTERNAL_SERVER_ERROR,
    NO_CONTENT,
    NOT_FOUND,
    UNAUTHORIZED,
)

from app import db
from app.models import User
from flask import Response, jsonify, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import use_args


class RegisterResource(Resource):
    """This resource is for registering."""

    @use_args(
        {
            "email": fields.Email(
                validate=validate.Length(
                    min=5, error="The email length have to be at least of 5 characters."
                ),
                required=True,
            ),
            "password": fields.Str(
                validate=validate.Length(
                    min=8,
                    error="The password length have to be at least of 8 characters.",
                ),
                required=True,
            ),
        },
        location="json",
    )
    def post(self, args):
        """This route allows to create a user."""

        email = request.json.get("email", None)
        password = request.json.get("password", None)

        # Check if a user already exists with this email.
        user = User.query.filter(User.email == email).one_or_none()
        if user:
            abort(
                CONFLICT,
                errors=[{"status": CONFLICT, "detail": "User already exists."}],
            )

        # Create the user.
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        try:
            db.session.commit()
            return Response(status=NO_CONTENT)
        # If the database insert fails for some reason we rollback.
        except IntegrityError:
            db.session.rollback()
            abort(
                INTERNAL_SERVER_ERROR,
                errors=[
                    {
                        "status": INTERNAL_SERVER_ERROR,
                        "detail": "Something went wrong while creating the new user.",
                    }
                ],
            )


class LoginResource(Resource):
    """This resource allows to get the jwt token by logging in."""

    @use_args(
        {
            "email": fields.Email(
                validate=validate.Length(
                    min=5, error="The email length have to be at least of 5 characters."
                ),
                required=True,
            ),
            "password": fields.Str(
                validate=validate.Length(
                    min=8,
                    error="The password length have to be at least of 8 characters.",
                ),
                required=True,
            ),
        },
        location="json",
    )
    def post(self, args):
        """This route give the JWT token.

        Returns:
            json: Return the JWT token.
        """
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        user = User.query.filter(User.email == email).one_or_none()
        # If the user doesn't exists or if the password isn't correct we abort.
        if not user:
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "User email doesn't exist."}],
            )
        if not user.check_password(password):
            abort(
                UNAUTHORIZED,
                errors=[{"status": UNAUTHORIZED, "detail": "Wrong password."}],
            )
        # Create the JWT token
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)
