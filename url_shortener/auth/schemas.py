from url_shortener.extensions import ma
from .models import User


class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        include_relationship = True
