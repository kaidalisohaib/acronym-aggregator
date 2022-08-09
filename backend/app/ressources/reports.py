from http.client import CREATED, INTERNAL_SERVER_ERROR

from app.models import Report, ReportSchema
from app.utils import generate_new_report
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort


class ReportsListResource(Resource):
    """This resource allow to create a new report and
    get a list of the report.
    """

    def get(self):
        """This route is to get a list of all the reports.

        Returns:
            List of the reports in a json:api format, e.g:
            {
                data:[
                    {
                        id: ...,
                        created_at: ...,
                        zip_path: ...,
                    },
                    ...
                ]
            }
        """
        reports = ReportSchema(many=True).dump(
            Report.query.order_by(Report.created_at).all()
        )
        return reports

    @jwt_required()
    def post(self):
        """This route allow to create a new report and generate
        the new zip file. (Require JWT token)

        Returns:
            The new reports in a json:api format.
            Not the file, the attributes.
        """
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
