from flask import make_response, jsonify
from aipkgs_requests import status

from aipkgs_core.responses.response import SuccessResponseInterface


class SuccessResponse(SuccessResponseInterface):
    @classmethod
    def forge_dict(cls, data: dict = None, status_code: int = None):
        response = {}
        if data:
            response.update(data)

        return make_response(jsonify(response), status_code or status.HTTP_200_OK)

    @classmethod
    def forge_raw(cls, status_code: int = None, **kwargs):
        response = {}
        response.update(kwargs)

        return make_response(jsonify(response), status_code or status.HTTP_200_OK)

    @classmethod
    def forge(cls, title: str = None, message: str = None, data: dict = None, status_code: int = None):
        response = {'title': title or 'success',
                    'message': message}
        if data:
            response.update(data)

        return make_response(jsonify(response), status_code or status.HTTP_200_OK)
