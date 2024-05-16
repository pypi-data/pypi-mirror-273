from aipkgs_requests import status
from flask import jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, get_jwt

from aipkgs_core.jwt.model import JWTModel


class JWTHelper:
    @staticmethod
    def fire(jwt: JWTManager):
        # The following callbacks are used for customizing jwt response/error messages.
        # The original ones may not be in a very pretty format (opinionated)
        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_data):
            model = JWTModel(jwt_data)
            if model.is_access():
                return make_response(jsonify({"message": "The token has expired.", "error": "token_expired"}), status.HTTP_401_UNAUTHORIZED)
            else:
                return make_response(jsonify({"message": "The token has expired.", "error": "token_expired"}), status.HTTP_401_UNAUTHORIZED)

        @jwt.invalid_token_loader
        def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
            return make_response(jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), status.HTTP_401_UNAUTHORIZED)

        @jwt.unauthorized_loader
        def missing_token_callback(error):
            return make_response(jsonify({
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }), status.HTTP_401_UNAUTHORIZED)

        @jwt.needs_fresh_token_loader
        def token_not_fresh_callback(jwt_header, jwt_data):
            return make_response(jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}), status.HTTP_401_UNAUTHORIZED)

        @jwt.revoked_token_loader
        def revoked_token_callback(jwt_header, jwt_data):  # called on blacklisted
            return make_response(jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), status.HTTP_401_UNAUTHORIZED)  # tokens


class AuthHelper:
    @staticmethod
    def generate_new_tokens(identity: str, fresh: bool = None, additional_claims: {} = None) -> (str, str):
        additional_claims = additional_claims if additional_claims else {}
        access_token = AuthHelper.generate_access_token(identity=identity, fresh=fresh or False, additional_claims=additional_claims)
        refresh_token = AuthHelper.generate_refresh_token(identity=identity, additional_claims=additional_claims)

        return access_token, refresh_token

    @staticmethod
    def generate_access_token(identity: str, fresh: bool = None, additional_claims: dict = None, additional_headers: dict = None) -> str:
        access_token = create_access_token(identity=identity, fresh=fresh or False, additional_claims=additional_claims, additional_headers=additional_headers)
        return access_token

    @staticmethod
    def generate_refresh_token(identity: str, additional_claims: dict = None) -> str:
        refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)
        return refresh_token
