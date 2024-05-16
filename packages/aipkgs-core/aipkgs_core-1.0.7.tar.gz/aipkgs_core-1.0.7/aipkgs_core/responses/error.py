from typing import Union

from aipkgs_requests import status
from flask import make_response, jsonify
from enum import Enum

from aipkgs_core.responses.response import ErrorResponseInterface


class ErrorResponse(ErrorResponseInterface):

    @classmethod
    def forge_dict(cls, data: dict = None, error_code: Union[int, Enum] = None, status_code: int = None):
        response = {}
        if data:
            response.update(data)

        if error_code:
            response['error_code'] = error_code.value if isinstance(error_code, Enum) else error_code

        return make_response(jsonify(response), status_code or status.HTTP_400_BAD_REQUEST)

    @classmethod
    def forge(cls, title: str = None, message: str = None, message_code: str = None, error_code: Union[int, Enum] = None, data: dict = None, status_code: int = None):
        response = {'title': title or 'Warning',
                    'message': message or 'Something went wrong'}
        if message_code:
            response['message_code'] = message_code

        if data:
            response.update(data)

        if error_code:
            response['error_code'] = error_code.value if isinstance(error_code, Enum) else error_code

        return make_response(jsonify(response), status_code or status.HTTP_400_BAD_REQUEST)

    # @classmethod
    # def forge_localized(cls, title_key: str = None, message_key: str = None, error_code: Union[int, Enum] = None, status_code: int = None):
    #     return ErrorResponse.forge(title=gettext(title_key) if title_key else None, message=gettext(message_key) if message_key else None, error_code=error_code,
    #                                status_code=status_code)

    @classmethod
    def not_found_error(cls, message: str = None):
        return ErrorResponse.forge(message=message or "Not found", status_code=status.HTTP_404_NOT_FOUND)