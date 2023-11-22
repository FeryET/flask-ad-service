from flask import Flask

from flask_ad_service.config import generate_app_config


def create_app() -> Flask:
    """Create the flask application."""
    app = Flask(__name__)
    app.config.update(generate_app_config())
    setup_db(app)
    return app


def setup_db(flask_app: Flask) -> None:
    """Set up the database for the flask app."""
    from flask_ad_service.database import db

    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()



if __name__ == "__main__":
    app = create_app()
