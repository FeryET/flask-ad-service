from flask import Flask

from flask_ad_service.config import generate_app_config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(generate_app_config())
    return app


if __name__ == "__main__":
    app = create_app()
