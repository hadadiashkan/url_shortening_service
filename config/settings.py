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

    MONGODB_SETTINGS = [
        {
            "db": env.str("MONGODB_DB"),
            "host": env.str("MONGODB_HOST"),
            "port": env.int("MONGODB_PORT"),
        }
    ]

    UPLOAD_DIR = env.str("UPLOAD_DIR")

    INSTALLED_RESOURCES = [
        "auth",
        "link",
    ]

    # To enable flask to catch package exceptions
    PROPAGATE_EXCEPTIONS = True

    SECRET_KEY = urandom(24)
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")

    SHORT_URL_LENGTH = 3
