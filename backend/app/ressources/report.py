from http.client import NOT_FOUND
from pathlib import Path

from app.models import Report
from flask import send_file
from flask_restful import Resource, abort


class ReportResource(Resource):
    """This resource allows to download a report in a zip format."""

    def get(self, version):
        """This route return the report in a zipfile

        Args:
            version (int): The version of the report, if the version < 1
            it becomes the latest version.

        Returns:
            The zip file containing the csv file.
        """
        report = None
        # If for some reason we receive a version less then 1 we
        # return the latest version.
        if version < 1:
            report = Report.query.order_by(Report.created_at.desc()).first()
        else:
            report = Report.query.get(version)

        # Check if the version is valid.
        if report is None:
            abort(
                NOT_FOUND,
                errors=[{"status": NOT_FOUND, "detail": "Couldn't find this version."}],
            )

        # Check if the report zip path still exists.
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
