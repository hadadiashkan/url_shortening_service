# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import importlib
import logging
import sys

from flask import Flask, render_template

from url_shortener import commands
from url_shortener.extensions import apispec, celery, jwt, db, ma


def create_app(config_object: str = "config.settings.Config", testing: bool = False) -> Flask:
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    :param testing: determine testing mode.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)

    if testing is True:
        app.config["TESTING"] = True

    register_extensions(app)
    register_cli(app)
    register_apispec(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    configure_logger(app)
    init_celery(app)
    return app


def register_extensions(app: Flask) -> None:
    """Register Flask extensions."""
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    return None


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    for installed_app_resources in app.config["INSTALLED_RESOURCES"]:
        app_resource = importlib.import_module(
            f"url_shortener.{installed_app_resources}.routes"
        )
        app.register_blueprint(app_resource.get_resources())
    return None


def register_errorhandlers(app: Flask) -> None:
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app: Flask) -> None:
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {}

    app.shell_context_processor(shell_context)


def register_cli(app: Flask) -> None:
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.init)


def configure_logger(app: Flask) -> None:
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_apispec(app: Flask) -> None:
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def init_celery(app: Flask = None) -> celery:
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
