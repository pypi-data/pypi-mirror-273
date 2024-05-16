from flask import make_response, jsonify

from aipkgs_requests import status

from aipkgs_core.responses.response import VerboseResponseInterface


class VerboseResponse(VerboseResponseInterface):
    @classmethod
    def forge(cls, data: dict = None, status_code: int = None):
        response = {}
        if data:
            response.update(data)

        return make_response(jsonify(response), status_code or status.HTTP_200_OK)
