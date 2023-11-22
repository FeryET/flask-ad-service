from flask import Flask
from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore

from flask_ad_service.config import generate_app_config


def create_app() -> Flask:
    """Create the flask application."""
    app = Flask(__name__)
    app.config.update(generate_app_config())
    setup_db(app)
    setup_flask_security(flask_app=app)
    return app


def setup_db(flask_app: Flask) -> None:
    """Set up the database for the flask app."""
    from flask_ad_service.database import db

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()


def setup_flask_security(flask_app: Flask) -> None:
    """Set up the flask security extension."""
    from flask_ad_service.database import db
    from flask_ad_service.model import RoleDBModel, UserDBModel

    user_datastore = SQLAlchemyUserDatastore(db, UserDBModel, RoleDBModel)  # type: ignore
    flask_app.security = Security(flask_app, user_datastore)  # type: ignore


if __name__ == "__main__":
    app = create_app()
