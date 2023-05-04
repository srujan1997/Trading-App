import json
import error_codes
from flask import Response


#####################
# Generic Responses #
#####################


def success_response(return_dict=None, status_code=200):
    """
    Description: Helper to create API success responses
    :param return_dict: dict
    :param status_code: int
    :return: API response (Flask response object)
    """
    if return_dict is None:
        return_dict = {}
    response = Response()
    to_return = {"success": True, "data": return_dict}
    response.data = json.dumps(to_return)
    response.headers["Content-type"] = "application/json"
    response.status_code = status_code
    return response


def error_response(error_code=error_codes.UNKNOWN, error_text="Something went wrong", status_code=400):
    """
    Description: Helper to create API error responses
    :param error_code: int
    :param error_text: string
    :param status_code: int
    :return: API response (Flask response object)
    """
    response = Response()
    to_return = {"success": False, "errors": [{"code": error_code, "text": error_text}]}
    response.data = json.dumps(to_return)
    response.headers["Content-type"] = "application/json"
    response.status_code = status_code
    return response


###########################
# Code Specific Responses #
###########################


def success(return_dict):  # Helper to create success response for API controller
    status_code = 200
    return success_response(return_dict, status_code)


def created(return_dict):  # Helper to create request created response for API controller
    status_code = 201
    return success_response(return_dict, status_code)


def bad_request(error_code=error_codes.INPUT_ERROR, error_text="Invalid Request"):
    # Helper to create bad request response for API controller
    status_code = 400
    return error_response(error_code, error_text, status_code)


def not_found(error_code=error_codes.RESOURCE_NOT_FOUND, error_text="Resource not found"):
    # Helper to create request not found response for API controller
    status_code = 404
    return error_response(error_code, error_text, status_code)


def internal_server_error(error_code=error_codes.UNKNOWN, error_text="Something went wrong"):
    # Helper to handle internal server errors for API controller.
    status_code = 500
    return error_response(error_code, error_text, status_code)