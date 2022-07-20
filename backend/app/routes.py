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


class AcronymListRessource(Resource):
    def get(self, acronym_id):
        acronym = Acronym.query.get(acronym_id)
        if acronym is None:
            abort(http_status_code=404, message="Acronym not found.")
        return acronym_shema.dump(acronym)


api.add_resource(AcronymListRessource, "/api/acronym/<int:acronym_id>")
api.add_resource(AcronymsListRessource, "/api/acronyms")
