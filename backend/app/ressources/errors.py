from http.client import UNPROCESSABLE_ENTITY

from app import app
from flask import jsonify


# Return validation errors as JSON
@app.errorhandler(422)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", None)
    errors = []
    if messages:
        for error in messages["json"]:
            for message in messages["json"][error]:
                errors.append({"status": UNPROCESSABLE_ENTITY, "detail": message})
    else:
        errors.append({"status": UNPROCESSABLE_ENTITY, "detail": "Invalid request."})
    print(err)
    if headers:
        return jsonify({"errors": errors}), err.code, headers
    else:
        return jsonify({"errors": errors}), err.code
