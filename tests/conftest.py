# Copyright 2019 by J. Christopher Wagner (jwag). All rights reserved.
import unittest.mock
from collections.abc import Generator
from typing import Any, Literal

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from flask_ad_service.config import generate_app_config
from flask_ad_service.database import db


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture(scope="session")
def _generate_testing_config() -> Generator[None, Any, None]:
    config = generate_app_config()
    config["TESTING"] = True
    config["WTF_CSRF_ENABLED"] = False
    # Our test emails/domain isn't necessarily valid
    config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}
    # Make this plaintext for most tests - reduces unit test time by 50%
    config["SECURITY_PASSWORD_HASH"] = "plaintext"

    config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with unittest.mock.patch(
        "flask_ad_service.app.generate_app_config", return_value=config
    ):
        yield


@pytest.fixture(scope="session")
def app(_generate_testing_config: None) -> Flask:
    """
    App for unittesting the package.
    """

    from flask_ad_service.app import create_app

    app = create_app()

    return app


@pytest.fixture(scope="session")
def _app_ctx(app: Flask) -> Generator[None, Any, None]:
    with app.app_context():
        yield


@pytest.fixture(scope="session")
def database(_app_ctx: None) -> Generator[SQLAlchemy, Any, None]:
    db.create_all()
    yield db
    db.session.rollback()
    db.drop_all()


@pytest.fixture(scope="module")
def db_test_session(
    _app_ctx: None,
    database: SQLAlchemy,
) -> Generator[Session, Any, None]:
    database.session.rollback()
    database.drop_all()
    database.session.close_all()
    database.create_all()
    from tests.faker.factories import (
        AdFactory,
        CommentFactory,
        RoleFactory,
        UserFactory,
    )

    for item in [AdFactory, RoleFactory, UserFactory, CommentFactory]:
        item._meta.reset_sequence()
    return database.session  # type: ignore


@pytest.fixture(scope="session")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="module")
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale() -> list[str]:
    return ["en_US"]


@pytest.fixture(scope="session", autouse=True)
def faker_seed() -> Literal[12345]:
    return 12345


@pytest.fixture()
def non_existant_user_id() -> Literal[1000]:
    return 1_000


@pytest.fixture()
def non_existant_ad_id() -> Literal[10000]:
    return 10_000


@pytest.fixture()
def non_existant_comment_id() -> Literal[100000]:
    return 100_000
