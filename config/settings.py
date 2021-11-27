# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from os import path, urandom


class Config:
    """Application Configuration."""

    from environs import Env

    env = Env()
    env.read_env()

    BASE_DIR = path.dirname(path.dirname(__file__))

    ENV = env.str("FLASK_ENV", default="production")
    DEBUG = ENV == "development"

    POSTGRES_USER = env.str("POSTGRES_USER")
    POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
    POSTGRES_DB = env.str("POSTGRES_DB")
    POSTGRES_HOST = env.str("POSTGRES_HOST")
    POSTGRES_PORT = env.int("POSTGRES_PORT")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_DIR = env.str("UPLOAD_DIR")

    INSTALLED_RESOURCES = [
        "auth",
        "link",
    ]

    # To enable flask to catch package exceptions
    PROPAGATE_EXCEPTIONS = True

    SECRET_KEY = urandom(24)
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")
