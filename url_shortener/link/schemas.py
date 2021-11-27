from url_shortener.extensions import ma
from .models import Link


class LinkSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Link
        include_fk = True
        include_relationships = True
        load_instance = True
