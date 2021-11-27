from flask import Blueprint
from flask import request
from flask_restful import Api, Resource

from .models import Link
from .schemas import LinkSchema
from ..extensions import db
from ..utils.response import custom_rest_response


class GenerateShortLink(Resource):
    def post(self):
        original_url = LinkSchema(only=("original_url",)).load(request.get_json())
        db.session.add(original_url)
        db.session.commit()
        return custom_rest_response(data={'link': LinkSchema().dump(original_url)}, status_code=201)


class ShortLink(Resource):
    def get(self, short_url):
        link = Link.query.filter(Link.short_url == short_url).first_or_404()
        link.visits += 1
        db.session.commit()
        return custom_rest_response(data={'link': LinkSchema().dump(link)})


def get_resources():
    """
    Returns app link resources.
    :param app: The Flask instance
    :return: App Login resources
    """
    blueprint = Blueprint("link", __name__, url_prefix="/api/v1")

    api = Api(blueprint)

    api.add_resource(GenerateShortLink, "/generate-link", endpoint="generate_link")
    api.add_resource(ShortLink, "/link/<short_url>", endpoint="get_original_link")

    return blueprint
