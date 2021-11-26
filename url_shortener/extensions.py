# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from celery import Celery
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

from url_shortener.utils.apispec import APISpecExt

mongo = MongoEngine()
db = SQLAlchemy()
apispec = APISpecExt()
ma = Marshmallow()
celery = Celery()
jwt = JWTManager()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
