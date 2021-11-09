import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from url_shortening.extensions import db
    from url_shortening.models import User

    click.echo("create user")
    user = User(
        username="admin", email="hadadi.ashkan@gmail.com", password="admin", active=True
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
