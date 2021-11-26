from flask import Blueprint
from flask import current_app as app
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Api, Resource

from url_shortener.auth.helpers import add_token_to_database, revoke_token
from url_shortener.extensions import apispec, pwd_context
from .models import User
from .schemas import LoginSchema
from ..utils.response import custom_rest_response

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


class Login(Resource):
    method_decorators = [jwt_required(refresh=True)]

    def post(self):
        """Authenticate user and return tokens

        ---
        post:
          tags:
            - auth
          summary: Authenticate a user
          description: Authenticates a user's credentials and returns tokens
          requestBody:
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    username:
                      type: string
                      example: myuser
                      required: true
                    password:
                      type: string
                      example: P4$$w0rd!
                      required: true
          responses:
            200:
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      access_token:
                        type: string
                        example: myaccesstoken
                      refresh_token:
                        type: string
                        example: myrefreshtoken
            400:
              description: bad request
          security: []
        """
        if not request.is_json:
            return custom_rest_response(error_msg={"msg": "Missing JSON in request"}, error_type='BadRequest',
                                        status_code=400)

        validated_data = LoginSchema(only=('username', 'password')).load(request.get_json())

        user = User.query.filter_by(username=validated_data.get('username')).first()
        if user is None or not pwd_context.verify(validated_data.get('password'), user.password):
            return custom_rest_response(error_msg={"msg": "Bad credentials"}, error_type='BadRequest',
                                        status_code=400)

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
        add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

        ret = {"access_token": access_token, "refresh_token": refresh_token}
        return custom_rest_response(data=ret, status_code=200)


class Refresh(Resource):
    method_decorators = [jwt_required(refresh=True)]

    def post(self):
        """Get an access token from a refresh token

        ---
        post:
          tags:
            - auth
          summary: Get an access token
          description: Get an access token by using a refresh token in the `Authorization` header
          responses:
            200:
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      access_token:
                        type: string
                        example: myaccesstoken
            400:
              description: bad request
            401:
              description: unauthorized
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        ret = {"access_token": access_token}
        add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
        return custom_rest_response(data=ret, status_code=200)


class RevokeAccessToken(Resource):
    method_decorators = [jwt_required()]

    def delete(self):
        """Revoke an access token

        ---
        delete:
          tags:
            - auth
          summary: Revoke an access token
          description: Revoke an access token
          responses:
            200:
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: token revoked
            400:
              description: bad request
            401:
              description: unauthorized
        """
        jti = get_jwt()["jti"]
        user_identity = get_jwt_identity()
        revoke_token(jti, user_identity)

        return custom_rest_response(data={"message": "token revoked"}, status_code=200)


class RevokeRefreshToken(Resource):
    method_decorators = [jwt_required(refresh=True)]

    def delete(self):
        """Revoke a refresh token, used mainly for logout

        ---
        delete:
          tags:
            - auth
          summary: Revoke a refresh token
          description: Revoke a refresh token, used mainly for logout
          responses:
            200:
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: token revoked
            400:
              description: bad request
            401:
              description: unauthorized
        """
        jti = get_jwt()["jti"]
        user_identity = get_jwt_identity()
        revoke_token(jti, user_identity)

        return custom_rest_response(data={"message": "token revoked"}, status_code=200)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=Login.as_view('login'), app=app)
    apispec.spec.path(view=Refresh.as_view('refresh'), app=app)
    apispec.spec.path(view=RevokeAccessToken.as_view('revoke_access'), app=app)
    apispec.spec.path(view=RevokeRefreshToken.as_view('revoke_refresh'), app=app)


def get_resources():
    """
    Returns app login resources.
    :param app: The Flask instance
    :return: App Login resources
    """
    blueprint = Blueprint("auth", __name__, url_prefix="/api/v1")

    api = Api(blueprint)

    api.add_resource(Login, "/login", endpoint="login")
    api.add_resource(Refresh, "/refresh", endpoint="refresh")
    api.add_resource(RevokeAccessToken, "/revoke-access", endpoint="revoke_access")
    api.add_resource(RevokeRefreshToken, "/revoke-refresh", endpoint="revoke_refresh")

    return blueprint
