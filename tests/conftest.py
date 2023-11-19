# Copyright 2019 by J. Christopher Wagner (jwag). All rights reserved.
from typing import Any
from unittest.mock import MagicMock

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from pytest_mock import MockerFixture


def generate_test_config() -> dict[Any, Any]:
    from flask_ad_service.config import generate_app_config

    config = generate_app_config()
    config["TESTING"] = True
    config["WTF_CSRF_ENABLED"] = False
    # Our test emails/domain isn't necessarily valid
    config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}
    # Make this plaintext for most tests - reduces unit test time by 50%
    config["SECURITY_PASSWORD_HASH"] = "plaintext"

    config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memory"

    return config


@pytest.fixture(scope="function")
def app(mocker: MockerFixture) -> "Flask":
    """
    App for unittesting the package.
    """

    from flask_ad_service.app import create_app

    config = generate_test_config()
    mocker.patch(
        "flask_ad_service.app.generate_app_config", new=MagicMock(return_value=config)
    )
    app = create_app()
    return app


@pytest.fixture(scope="function")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
