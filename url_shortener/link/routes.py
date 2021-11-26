from flask import Blueprint
from flask_restful import Api


def get_resources():
    """
    Returns app link resources.
    :param app: The Flask instance
    :return: App Login resources
    """
    blueprint = Blueprint("link", __name__, url_prefix="/api/v1")

    api = Api(blueprint)

    api.add_resource(Login, "/login", endpoint="login")

    return blueprint
