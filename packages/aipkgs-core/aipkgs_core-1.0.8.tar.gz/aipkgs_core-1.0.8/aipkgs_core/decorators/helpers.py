from functools import wraps

from aipkgs_requests import status
from flask_jwt_extended import get_jwt
from flask import request
import inspect

from aipkgs_core.responses.error import ErrorResponse


class FlaskDecorators:
    @staticmethod
    def is_admin():
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                claims = get_jwt()
                if not claims["is_admin"]:
                    return ErrorResponse.forge(message="Admin privilege required.",
                                               status_code=status.HTTP_401_UNAUTHORIZED)
                return func(*args, **kwargs)

            return wrapper

        return decorator
