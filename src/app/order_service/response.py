import json
from flask import Response


#####################
# Generic Responses #
#####################


def success_response(return_dict=None, status_code=200):
    if return_dict is None:
        return_dict = {}
    response = Response()
    to_return = {"success": True, "data": return_dict}
    response.data = json.dumps(to_return)
    response.headers["Content-type"] = "application/json"
    response.status_code = status_code
    return response


def error_response(error_code=2000, error_text="Something went wrong", status_code=400):
    response = Response()
    to_return = {"success": False, "errors": [{"code": error_code, "text": error_text}]}
    response.data = json.dumps(to_return)
    response.headers["Content-type"] = "application/json"
    response.status_code = status_code
    return response
