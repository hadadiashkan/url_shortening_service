import string
from datetime import datetime
from random import choices

from flask import current_app

from url_shortener.extensions import db

SHORT_URL_LENGTH = current_app.config.get('SHORT_URL_LENGTH')


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(SHORT_URL_LENGTH), unique=True)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=False), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=SHORT_URL_LENGTH))

        existing_link = self.query.filter(self.short_url == short_url).exists()

        return self.generate_short_link() if existing_link else short_url
