import csv
import os
from http.client import (
    BAD_REQUEST,
    CONFLICT,
    INTERNAL_SERVER_ERROR,
    NO_CONTENT,
    NOT_FOUND,
)
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app import api, db
from app.models import Acronym, AcronymSchema, Report, ReportSchema
from flask import Response, request, send_file
from flask_restful import Resource, abort
from flask_sqlalchemy import BaseQuery
from psycopg2 import errorcodes
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
        return results

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
            return AcronymSchema().dump(new_acronym), 201
        except IntegrityError as err:
            db.session.rollback()
            match err.orig.pgcode:
                case errorcodes.UNIQUE_VIOLATION:
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
        return AcronymSchema().dump(acronym)

    def patch(self, acronym_id):
        request.json["data"].pop("id")

        errors = AcronymSchema().validate(request.json)
        if errors:
            abort(BAD_REQUEST, errors=errors["errors"])

        attributes = request.json["data"]["attributes"]

        acronym = Acronym.query.get(acronym_id)
        if acronym is None:
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "Acronym not found."}],
            )
        acronym.acronym = attributes["acronym"]
        acronym.meaning = attributes["meaning"]
        acronym.comment = attributes["comment"]
        acronym.company = attributes["company"]
        acronym.last_modified_by = "email@email.com"

        try:
            db.session.commit()
            return AcronymSchema().dump(acronym)
        except IntegrityError as err:
            db.session.rollback()
            match err.orig.pgcode:
                case errorcodes.UNIQUE_VIOLATION:
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

    def delete(self, acronym_id):
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
        except Exception:
            db.session.rollback()


class ReportsListRessource(Resource):
    def get(self):
        reports = ReportSchema(many=True).dump(
            Report.query.order_by(Report.created_at).all()
        )
        return reports

    def post(self):
        try:
            new_id = generate_new_report()
            return (
                ReportSchema().dump(Report.query.get(new_id)),
                201,
            )
        except Exception:
            abort(
                INTERNAL_SERVER_ERROR,
                errors=[
                    {
                        "status": INTERNAL_SERVER_ERROR,
                        "details": "Internal error, could not create a new report.",
                    }
                ],
            )


class ReportRessource(Resource):
    def get(self, version):
        """This route return the latest report in a zipfile

        Keyword arguments:
        version -- Version number, if not given then -1 means latest
        Return: The compressed reported data
        """
        report = None
        if version < 1:
            report = Report.query.order_by(Report.created_at.desc()).first()
        else:
            report = Report.query.get(version)

        if report is None:
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "Couldn't find this version."}],
            )

        if not Path(report.zip_path).exists():
            abort(
                NOT_FOUND,
                errors=[
                    {"status": NOT_FOUND, "detail": "This report file no longer exist."}
                ],
            )
        zip_path = Path(report.zip_path)
        return send_file(zip_path.absolute(), attachment_filename=zip_path.name)


api.add_resource(AcronymRessource, "/api/acronyms/<int:acronym_id>")
api.add_resource(AcronymsListRessource, "/api/acronyms")

api.add_resource(ReportRessource, "/api/reports/<int:version>")
api.add_resource(ReportsListRessource, "/api/reports")


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
            # I only take the name of the column inside the square brackets
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


def generate_new_report():
    # Create temp dir if it doesn't exist
    temp_path = Path("./tmp")
    temp_path.mkdir(exist_ok=True)

    new_report = Report(temp_path.absolute())
    db.session.add(new_report)
    db.session.commit()

    # Latest version number
    new_version = new_report.id

    db.session.rollback()

    # Create the reports dir if it doesn't exist
    reports_path = Path("./reports")
    reports_path.mkdir(exist_ok=True)

    # New csv file
    new_csv_temp_path: Path = Path(f"{temp_path}/all_acronyms_v{new_version}.csv")
    # New pdf file
    new_pdf_temp_path: Path = Path(f"{temp_path}/all_acronyms_v{new_version}.pdf")
    # New report zip file
    new_zip_path: Path = Path(f"{reports_path}/all_acronyms_v{new_version}.zip")
    try:
        create_and_fill_csv_file(str(new_csv_temp_path.absolute()))
        create_and_fill_pdf_file(str(new_pdf_temp_path.absolute()))
        # Compress the generated files
        with ZipFile(new_zip_path, mode="w") as zipfile:
            if new_csv_temp_path.exists():
                zipfile.write(
                    new_csv_temp_path.absolute(),
                    new_csv_temp_path.name,
                    compress_type=ZIP_DEFLATED,
                )

            if new_pdf_temp_path.exists():
                zipfile.write(
                    new_pdf_temp_path.absolute(),
                    new_pdf_temp_path.name,
                    compress_type=ZIP_DEFLATED,
                )
        Report.query.get(new_version).zip_path = str(new_zip_path.absolute())
        db.session.commit()
        return new_version
    except Exception:
        db.session.rollback()
        raise Exception("Could't generate a new report.")
    finally:
        if new_csv_temp_path.exists():
            os.remove(new_csv_temp_path)
        if new_pdf_temp_path.exists():
            os.remove(new_pdf_temp_path)


def create_and_fill_csv_file(filepath: Path):
    "Fill a csv file with all the acronyms"
    with open(filepath, "w") as file:
        out = csv.writer(file)
        out.writerow(Acronym.__table__.columns.keys())
        # Write all rows into the file
        for acronym in Acronym.query.all():
            out.writerow(
                [
                    getattr(acronym, column_name)
                    for column_name in Acronym.__table__.columns.keys()
                ]
            )


# For now this function does nothing because I didn't found a library
# to generate a good pdf file
def create_and_fill_pdf_file(filepath: Path):
    pass
