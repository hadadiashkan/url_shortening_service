import pytest
from mongoengine import disconnect_all

from url_shortener.app import create_app


@pytest.fixture
def app():
    """Create application for the tests."""
    disconnect_all()
    app = create_app(testing=True)
    return app
