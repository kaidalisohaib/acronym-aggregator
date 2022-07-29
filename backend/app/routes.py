from http.client import BAD_REQUEST, CONFLICT

import psycopg2
from app import api, db
from app.models import Acronym, AcronymSchema
from flask import jsonify, request
from flask_restful import Resource, abort
from flask_sqlalchemy import BaseQuery
from sqlalchemy import String, cast
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import use_args


class AcronymsListRessource(Resource):
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
                items_count: 50
                pages_count: 100
            }
        }
        - "has_next": If there is a page after this one
        - "has_prev": If there is a page before this one
        - "items_count": Number of acronym returned in the data
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
            metadata["pages_count"] = pagination.pages
            metadata["has_prev"] = pagination.has_prev
            metadata["has_next"] = pagination.has_next
        else:
            acronyms = query_object.all()

        results = AcronymSchema(many=True).dump(acronyms)
        metadata["items_count"] = len(acronyms)
        if metadata:
            results["meta"] = metadata
        return jsonify(results)

    def post(self):
        errors = AcronymSchema().validate(request.json)
        if errors:
            abort(BAD_REQUEST, errors=errors["errors"])

        attributes = request.json["data"]["attributes"]
        new_acronym = Acronym(
            attributes["acronym"],
            attributes["meaning"],
            attributes["comment"],
            attributes["company"],
            "email@email.com",
        )
        db.session.add(new_acronym)
        try:
            db.session.commit()
            return jsonify(AcronymSchema().dump(new_acronym))
        except IntegrityError as err:
            db.session.rollback()
            match err.orig.pgcode:
                case psycopg2.errorcodes.UNIQUE_VIOLATION:
                    abort(
                        CONFLICT,
                        errors=[
                            {
                                "status": CONFLICT,
                                "detail": "Acronym with the same details \
                                    already exist in the database.",
                            }
                        ],
                    )


class AcronymRessource(Resource):
    def get(self, acronym_id):
        acronym = Acronym.query.get(acronym_id)
        if acronym is None:
            abort(http_status_code=404, message="Acronym not found.")
        return jsonify(AcronymSchema().dump(acronym))

    def patch(self, acronym_id):
        request.json["data"].pop("id")

        errors = AcronymSchema().validate(request.json)
        if errors:
            abort(BAD_REQUEST, errors=errors["errors"])

        attributes = request.json["data"]["attributes"]

        acronym = Acronym.query.get(acronym_id)
        acronym.acronym = attributes["acronym"]
        acronym.meaning = attributes["meaning"]
        acronym.comment = attributes["comment"]
        acronym.company = attributes["company"]
        acronym.last_modified_by = "email@email.com"

        try:
            db.session.commit()
            return jsonify(AcronymSchema().dump(acronym))
        except IntegrityError as err:
            db.session.rollback()
            match err.orig.pgcode:
                case psycopg2.errorcodes.UNIQUE_VIOLATION:
                    abort(
                        CONFLICT,
                        errors=[
                            {
                                "status": CONFLICT,
                                "detail": "Acronym with the same details\
                                    already exist in the database.",
                            }
                        ],
                    )


api.add_resource(AcronymRessource, "/api/acronyms/<int:acronym_id>")
api.add_resource(AcronymsListRessource, "/api/acronyms")


def build_acronyms_filter_sort_query(args) -> BaseQuery:
    """Build a query with the filters given and the column to sort

    Keyword arguments:
    argument -- Parameters of the api request
    Return: return_description
    For each column we verify if the args contains the proper keyword
        If yes we add the filter
        Else we continue to the next column
    """

    query_object = Acronym.query
    # Adding filters to the query
    for key, value in args.items():
        if key.startswith("filter"):
            # 7 is the length of the word "filter" + 1
            column_name = key[7:-1]
            column = getattr(Acronym, column_name)
            query_object = query_object.filter(
                cast(column, String).contains(str(value))
            )
    # Adding the sorting to the query
    if "sorting[column]" in args:
        if args["sorting[ascending]"]:
            query_object = query_object.order_by(
                getattr(Acronym, args["sorting[column]"]).asc(), Acronym.id
            )
        else:
            query_object = query_object.order_by(
                getattr(Acronym, args["sorting[column]"]).desc(), Acronym.id
            )
    else:
        query_object = query_object.order_by(Acronym.id)

    return query_object
