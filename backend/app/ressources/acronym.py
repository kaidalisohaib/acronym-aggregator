from http.client import BAD_REQUEST, CONFLICT, NO_CONTENT, NOT_FOUND

from app import db
from app.models import Acronym, AcronymSchema
from flask import Response, request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, abort
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError


class AcronymResource(Resource):
    """This resource provide a way to get an acronym by id,
    update an acronym by id and delete an acronym.
    """

    def get(self, acronym_id):
        """This route returns an acronym.

        Args:
            acronym_id (int): The id of the wanted acronym.

        Returns:
            The acronym in a json:api format..
        """
        acronym = Acronym.query.get(acronym_id)
        if acronym is None:
            abort(http_status_code=404, message="Acronym not found.")
        return AcronymSchema().dump(acronym)

    @jwt_required()
    def patch(self, acronym_id):
        """This route update an acronym. (Require JWT token)

        Args:
            acronym_id (int): The id of the wanted acronym.
        Receive:
            The new acronym attributes. E.g:
                {
                    data:{
                        id: null,
                        acronym: ..., (required)
                        meaning: ..., (required)
                        comment: ...,
                        company: ..., (required)
                        created_at: null,
                        last_modified_at: null,
                        created_by: null,
                        last_modified_by: null,
                    }
                }
        Returns:
            The updated acronym in a json:api format.
        """
        request.json["data"].pop("id")

        # Check if the received acronym attributes are valid.
        errors = AcronymSchema().validate(request.json)
        if errors:
            abort(BAD_REQUEST, errors=errors["errors"])

        attributes = request.json["data"]["attributes"]

        # Check if the acronym exist with the received id.
        acronym = Acronym.query.get(acronym_id)
        if acronym is None:
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "Acronym not found."}],
            )

        # Update the acronym attributes
        acronym.acronym = attributes["acronym"]
        acronym.meaning = attributes["meaning"]
        acronym.comment = attributes["comment"]
        acronym.company = attributes["company"]
        acronym.set_modified_user(current_user)

        try:
            db.session.commit()
            return AcronymSchema().dump(acronym)
        # If the attributes already exist an Exception is raised (UniqueConstraint)
        except IntegrityError as err:
            db.session.rollback()
            match err.orig.pgcode:
                case errorcodes.UNIQUE_VIOLATION:
                    abort(
                        CONFLICT,
                        errors=[
                            {
                                "status": CONFLICT,
                                "detail": (
                                    "Acronym with the same details already"
                                    " exists in the database."
                                ),
                            }
                        ],
                    )

    @jwt_required()
    def delete(self, acronym_id):
        """This route delete an acronym. (Require JWT token)

        Args:
            acronym_id (int): The id of the wanted acronym
        """
        # Check if the acronym exists.
        acronym_to_delete = Acronym.query.filter(Acronym.id == acronym_id)
        if acronym_to_delete.count() == 0:
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "Acronym not found."}],
            )
        acronym_to_delete.delete()
        try:
            db.session.commit()
            return Response(status=NO_CONTENT)
        # If for some reason something fail we rollback
        except IntegrityError:
            db.session.rollback()
