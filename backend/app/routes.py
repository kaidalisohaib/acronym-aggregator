import csv
import io
from http.client import (
    ACCEPTED,
    BAD_REQUEST,
    CONFLICT,
    CREATED,
    INTERNAL_SERVER_ERROR,
    NO_CONTENT,
    NOT_FOUND,
    UNAUTHORIZED,
)
from pathlib import Path

from app import api, app, db, jwt
from app.models import Acronym, AcronymSchema, Report, ReportSchema, User
from flask import Response, jsonify, request, send_file
from flask_jwt_extended import create_access_token, current_user, jwt_required
from flask_restful import Resource, abort
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError
from webargs import fields, validate
from webargs.flaskparser import use_args

from .utils import (
    allowed_file,
    build_acronyms_filter_sort_query,
    generate_new_report,
    string_is_empty,
)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    print("tSERSDFLJALS")
    identity = jwt_data["sub"]
    return User.query.get(identity)


class AcronymsListResource(Resource):
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

    @jwt_required()
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
            current_user,
        )
        db.session.add(new_acronym)
        try:
            db.session.commit()
            return AcronymSchema().dump(new_acronym), CREATED
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


class AcronymResource(Resource):
    def get(self, acronym_id):
        acronym = Acronym.query.get(acronym_id)
        if acronym is None:
            abort(http_status_code=404, message="Acronym not found.")
        return AcronymSchema().dump(acronym)

    @jwt_required()
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
        acronym.set_modified_user(current_user)

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
                                "detail": (
                                    "Acronym with the same details already"
                                    " exists in the database."
                                ),
                            }
                        ],
                    )

    @jwt_required()
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
        except IntegrityError:
            db.session.rollback()


class ReportsListResource(Resource):
    def get(self):
        reports = ReportSchema(many=True).dump(
            Report.query.order_by(Report.created_at).all()
        )
        return reports

    @jwt_required()
    def post(self):
        try:
            new_id = generate_new_report()
            return (
                ReportSchema().dump(Report.query.get(new_id)),
                CREATED,
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


class ReportResource(Resource):
    def get(self, version):
        """This route return the report in a zipfile

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
                    {
                        "status": NOT_FOUND,
                        "detail": "This report file no longer exists.",
                    }
                ],
            )
        zip_path = Path(report.zip_path)
        return send_file(zip_path.absolute(), attachment_filename=zip_path.name)


class UploadCSVResource(Resource):
    @jwt_required()
    def post(self):
        pass
        print(request.files)
        print(request.files["file"])
        if "file" not in request.files:
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "File part is missing."}],
            )

        file = request.files["file"]
        if file.filename == "":
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "No file selected."}],
            )

        if file and not allowed_file(file.filename):
            abort(
                BAD_REQUEST,
                errors=[
                    {"status": BAD_REQUEST, "detail": "File extension not allowed"}
                ],
            )

        file_data = io.StringIO(file.read().decode("latin-1"))
        reader = csv.reader(file_data)
        rows = list(reader)
        skipped_rows = []
        if not rows:
            abort(
                BAD_REQUEST,
                errors=[{"status": BAD_REQUEST, "detail": "No rows in file."}],
            )
        added_rows = 0
        for index, row in enumerate(rows):
            if len(row) < 4:
                skipped_rows.append(index)
                continue
            if (
                string_is_empty(row[0])
                or string_is_empty(row[1])
                or string_is_empty(row[3])
            ):
                skipped_rows.append(index)
                continue
            try:
                new_acronym = Acronym(row[0], row[1], row[2], row[3], current_user)
                db.session.add(new_acronym)
                db.session.commit()
                added_rows += 1
            except IntegrityError:
                skipped_rows.append(index)
                db.session.rollback()
        file_data.close()
        if skipped_rows:
            return {
                "skippedRows": skipped_rows,
                "addedRows": added_rows,
                "totalRows": len(rows),
            }, ACCEPTED

        return {
            "skippedRows": skipped_rows,
            "addedRows": added_rows,
            "totalRows": len(rows),
        }, CREATED


class RegisterResource(Resource):
    def post(self):
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        user = User.query.filter(User.email == email).one_or_none()
        if user:
            abort(
                CONFLICT,
                errors=[{"status": CONFLICT, "detail": "User already exists."}],
            )

        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        try:
            db.session.commit()
            return Response(status=NO_CONTENT)
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
    def post(self):
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        user = User.query.filter(User.email == email).one_or_none()

        if not user or not user.check_password(password):
            abort(
                UNAUTHORIZED,
                errors=[{"status": UNAUTHORIZED, "detail": "Wrong email or password"}],
            )

        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)


api.add_resource(AcronymResource, "/api/acronyms/<int:acronym_id>")
api.add_resource(AcronymsListResource, "/api/acronyms")

api.add_resource(ReportResource, "/api/reports/<int:version>")
api.add_resource(ReportsListResource, "/api/reports")

api.add_resource(UploadCSVResource, "/api/upload")

api.add_resource(RegisterResource, "/api/register")
api.add_resource(LoginResource, "/api/login")
