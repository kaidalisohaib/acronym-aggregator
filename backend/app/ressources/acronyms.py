from http.client import BAD_REQUEST, CONFLICT, CREATED

from app import db
from app.models import Acronym, AcronymSchema
from app.utils import build_acronyms_filter_sort_query
from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, abort
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import use_args


class AcronymsListResource(Resource):
    """This resource give access to get a list of acronyms with filters on columns,
    one column sorting and also to create a new acronym.
    """

    @use_args(
        {
            "display_per_page": fields.Int(
                validate=validate.Range(min=1), required=False
            ),
            "page": fields.Int(
                missing=1, validate=validate.Range(min=1), required=False
            ),
            "sorting[column]": fields.Str(
                validate=validate.OneOf(choices=Acronym.__table__.columns.keys()),
                required=False,
            ),
            "sorting[ascending]": fields.Bool(missing=True, required=False),
            "filter[id]": fields.Int(validate=validate.Range(min=1), required=False),
            "filter[acronym]": fields.Str(
                validate=validate.Length(min=1), required=False
            ),
            "filter[meaning]": fields.Str(
                validate=validate.Length(min=1), required=False
            ),
            "filter[comment]": fields.Str(
                validate=validate.Length(min=1), required=False
            ),
            "filter[company]": fields.Str(
                validate=validate.Length(min=1), required=False
            ),
            "filter[created_at]": fields.Str(
                validate=validate.Length(min=1), required=False
            ),
            "filter[last_modified_at]": fields.Str(
                validate=validate.Length(min=1), required=False
            ),
            "filter[created_by]": fields.Str(
                validate=validate.Length(min=1), required=False
            ),
            "filter[updated_by]": fields.Str(
                validate=validate.Length(min=1), required=False
            ),
        },
        location="query",
    )
    def get(self, args):
        """This route returns all the acronyms unless argument display_per_page
        is given which paginate.

        - Optional arguments:
            - "display_per_page": Number of element per page
            - "page": Page number (default=1)
            - "filter[id]": Filter value for the id column
            - "filter[acronym]": Filter value for the acronym column
            - "filter[meaning]": Filter value for the meaning column
            - "filter[comment]": Filter value for the comment column
            - "filter[company]": Filter value for the company column
            - "filter[created_at]": Filter value for the created_at column
            - "filter[last_modified_at]": Filter value for the last_modified_at column
            - "filter[created_by]": Filter value for the created_by column
            - "filter[updated_by]": Filter value for the updated_by column

        Returns a dictionnary in this form:

        {
            "data": [all the acronyms],
            "meta": {
                has_next: true
                has_prev: true
                item_count: 50
                page_count: 100
            }
        }
        - "has_next": If there is a page after this one
        - "has_prev": If there is a page before this one
        - "item_count": Number of acronym returned in the data
        - "page_count": Number of page in total with this number of acronym per page
        """
        acronyms = []
        metadata = {}
        query_object = build_acronyms_filter_sort_query(args)
        if "display_per_page" in args:
            page = args["page"]
            display_per_page = args["display_per_page"]
            pagination = query_object.paginate(page, display_per_page, False)
            acronyms = pagination.items
            metadata["page_count"] = pagination.pages
            metadata["has_prev"] = pagination.has_prev
            metadata["has_next"] = pagination.has_next
        else:
            acronyms = query_object.all()

        results = AcronymSchema(many=True).dump(acronyms)
        metadata["item_count"] = len(acronyms)
        if metadata:
            results["meta"] = metadata
        return results

    @jwt_required()
    def post(self):
        """This route create an acronym. (Require JWT token)

        Receive:
            A new acronym in a json:api format.
        Returns:
            The new acronym in a json:api format.
        """
        # Check if the acronym is valid
        errors = AcronymSchema().validate(request.json)
        if errors:
            abort(BAD_REQUEST, errors=errors["errors"])

        attributes = request.json["data"]["attributes"]
        # Create the new acronym
        new_acronym = Acronym(
            attributes["acronym"],
            attributes["meaning"],
            attributes["comment"],
            attributes["company"],
            current_user,
        )
        db.session.add(new_acronym)
        try:
            db.session.commit()
            return AcronymSchema().dump(new_acronym), CREATED
        # If a duplicate exist or if anything goes wrong we rollback.
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
