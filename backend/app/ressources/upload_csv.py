import csv
import io
from http.client import ACCEPTED, BAD_REQUEST, CREATED, NOT_FOUND

from app import db
from app.models import Acronym
from app.utils import allowed_upload_file, string_is_empty
from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError


class UploadCSVResource(Resource):
    """This resource allow to upload a csv file and
    add all the rows."""

    @jwt_required()
    def post(self):
        """This route is made to add all the rows in a csv
        file into the database.

        Returns:
            Information about the process, e.g:
            {
                skippedRows: ...,
                addedRows: ...,
                totalRows: ...,
            }
        """
        # Check if there is a file part
        if "file" not in request.files:
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "File part is missing."}],
            )

        # Check if the file part is not empty/no file
        file = request.files["file"]
        if file.filename == "":
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "No file selected."}],
            )

        # Check if file extension is allowed
        if file and not allowed_upload_file(file.filename):
            abort(
                BAD_REQUEST,
                errors=[
                    {"status": BAD_REQUEST, "detail": "File extension not allowed"}
                ],
            )

        # Read file
        file_data = io.StringIO(file.read().decode("latin-1"))
        reader = csv.reader(file_data)
        rows = list(reader)
        skipped_rows = []
        # Check the file is empty/no rows
        if not rows:
            abort(
                BAD_REQUEST,
                errors=[{"status": BAD_REQUEST, "detail": "No rows in file."}],
            )
        added_rows = 0
        # For every rows, if all the condition are true then the acronym is added
        # unless a duplicate exists.
        # Each row that isn't getting added is marked as skipped
        for index, row in enumerate(rows):
            if len(row) < 4:
                skipped_rows.append(index + 1)
                continue
            if (
                string_is_empty(row[0])
                or string_is_empty(row[1])
                or string_is_empty(row[3])
            ):
                skipped_rows.append(index + 1)
                continue
            try:
                new_acronym = Acronym(row[0], row[1], row[2], row[3], current_user)
                db.session.add(new_acronym)
                db.session.commit()
                added_rows += 1
            except IntegrityError:
                skipped_rows.append(index + 1)
                db.session.rollback()
        file_data.close()

        # Return the skipped rows, added rows and total rows
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
