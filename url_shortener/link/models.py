import string
from datetime import datetime
from random import choices

from url_shortener.extensions import db


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(5), unique=True)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=False), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=5))

        existing_link = self.query.filter(self.short_url == short_url).first()
        return self.generate_short_link() if existing_link else short_url
