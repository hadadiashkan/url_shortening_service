"""Simple blocklist implementation using database
Using database may not be your prefered solution to handle blocklist in your
final application, but remember that's just a cookiecutter template. Feel free
to dump this code and adapt it for your needs.
For this reason, we don't include advanced tokens management in this
example (view all tokens for a user, revoke from api, etc.)
If we choose to use database to handle blocklist in this example, it's mainly
because it will allow you to run the example without needing to setup anything else
like a redis or a memcached server.
This example is heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/blocklist_database.py
"""
from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from url_shortener.extensions import db, pwd_context


class TokenBlocklist(db.Model):
    """Blocklist representation"""

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", lazy="joined")


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime(timezone=False), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=False), onupdate=datetime.utcnow)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username
