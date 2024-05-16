from functools import wraps

from flask_jwt_extended import get_jwt
from flask import request
import inspect


def is_admin():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if not claims["is_admin"]:
                return ErrorResponse.forge(message=gettext('admin_privilege_required'),
                                           status_code=status.HTTP_401_UNAUTHORIZED)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_headers():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # region language
            provided_locale = request.headers.get('Accept-Language')
            if not provided_locale:
                return ErrorResponse.forge(message=gettext('missing_accept_language'))

            final_locale: str = ''
            locale_array: list = provided_locale.split("-")
            provided_language: str = 'en'
            if len(locale_array) > 0:
                provided_language = locale_array[0]

            lang_compatibility_ratio: float = 0  # 0 none, 0.5 partial, 1 full
            available: bool = next((True for locale in localization_helper.accepted_locales if provided_locale == locale['locale']), False)
            if available:
                lang_compatibility_ratio = 1.0
                final_locale = provided_locale
            else:
                available: bool = next((True for locale in localization_helper.accepted_locales if provided_language in locale['language']), False)
                if available:
                    lang_compatibility_ratio = 0.5
                else:
                    lang_compatibility_ratio = 0

            if lang_compatibility_ratio == 0:
                final_locale = constants.default_locale
            elif lang_compatibility_ratio == 0.5:
                if 'en' in provided_language:
                    final_locale = 'en-US'
                elif 'ar' in provided_language:
                    final_locale = 'ar-LB'
            # return ErrorResponse.forge(message=gettext('invalid_accept_language'))
            # endregion

            # region client
            client_os = request.headers.get('Client-OS')
            if not client_os:
                return ErrorResponse.forge(message=gettext('missing_client_os'))

            client_os_version = request.headers.get('Client-OS-Version')
            if not client_os_version:
                return ErrorResponse.forge(message=gettext('missing_client_os_version'))

            client_timezone = request.headers.get('Client-Timezone')
            if not client_timezone:
                return ErrorResponse.forge(message=gettext('missing_client_timezone'))

            client_model = request.headers.get('Client-Model')
            if not client_model:
                return ErrorResponse.forge(message=gettext('missing_client_model'))
            # endregion

            # region app
            app_version = request.headers.get('App-Version')
            if not app_version:
                return ErrorResponse.forge(message=gettext('missing_app_version'))
            # endregion

            headers: HeadersModel = HeadersModel(locale=final_locale,
                                                 client_os=client_os,
                                                 client_os_version=client_os_version,
                                                 client_timezone=client_timezone.replace(' ', ''),
                                                 client_model=client_model,
                                                 app_version=app_version)

            # check if function has argument "header"
            full_arg = inspect.getfullargspec(func)  # sig = inspect.signature(func)

            if 'headers' in full_arg.args:
                return func(*args, **kwargs, headers=headers)

            return func(*args, **kwargs)

        return wrapper

    return decorator

# class FlaskDecorators:
#     @staticmethod




# def superuser(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#
#         if not g.user.superuser:
#             flash("You do not have permission to view that page", "warning")
#             abort(404)
#
#         return f(*args, **kwargs)
#
#     return decorated_function
