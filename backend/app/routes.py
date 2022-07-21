from app import api
from app.models import Acronym, acronym_shema, acronyms_shema
from flask import jsonify, request
from flask_restful import Resource, abort
from webargs import fields
from webargs.flaskparser import use_args


class AcronymsListRessource(Resource):
    @use_args(
        {
            "display_per_page": fields.Int(required=False),
            "page": fields.Int(missing=1, required=False),
        },
        location="query",
    )
    def get(self, args):
        """This route returns all the acronyms unless argument display_per_page
        is given which paginate.

        - Optional arguments:
            - "display_per_page": Number of element per page
            - "page": Page number (default=1)

        Returns a dictionnary in this form:

        {
            "acronyms":[all the acronyms],
            "next_url": "http://localhost:5000/api/acronyms?display_per_page=4&page=2",
            "prev_url": null
        }
        - "next_url": URL of the next page, if there is none then null is returned
        - "prev_url": URL of the previous page, if there is none then null is returned
        """

        acronyms = []
        prev_url = None
        next_url = None
        if "display_per_page" in args:
            page = args["page"]
            display_per_page = args["display_per_page"]
            pagination = Acronym.query.order_by(Acronym.acronym).paginate(
                page, display_per_page, False
            )
            acronyms = pagination.items
            if pagination.has_prev:
                prev_url = "{}?display_per_page={}&page={}".format(
                    request.base_url, display_per_page, page - 1
                )
            if pagination.has_next:
                next_url = "{}?display_per_page={}&page={}".format(
                    request.base_url, display_per_page, page + 1
                )
        else:
            acronyms = Acronym.query.order_by(Acronym.acronym).all()
        results = {"acronyms": acronyms_shema.dump(acronyms)}
        results["next_url"] = next_url
        results["prev_url"] = prev_url
        return jsonify(results)


class AcronymRessource(Resource):
    def get(self, acronym_id):
        acronym = Acronym.query.get(acronym_id)
        if acronym is None:
            abort(http_status_code=404, message="Acronym not found.")
        return acronym_shema.dump(acronym)


api.add_resource(AcronymRessource, "/api/acronym/<int:acronym_id>")
api.add_resource(AcronymsListRessource, "/api/acronyms")
