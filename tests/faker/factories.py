import uuid

import factory
from factory.alchemy import SQLAlchemyModelFactory
from flask import current_app
from sqlalchemy.orm import scoped_session

from flask_ad_service.database import db
from flask_ad_service.model import AdDBModel, CommentDBModel, RoleDBModel, UserDBModel


def make_session():
    return scoped_session(
        lambda: current_app.extensions["sqlalchemy"].db.session,  # type: ignore
        scopefunc=lambda: current_app.extensions["sqlalchemy"].db.session,
    )


class CommonMeta:
    sqlalchemy_session = db.session
    # sqlalchemy_session_factory = make_session
    sqlalchemy_session_persistence = "commit"
    sqlalchemy_get_or_create = ("id",)


class RoleFactory(SQLAlchemyModelFactory):
    class Meta(CommonMeta):
        model = RoleDBModel

    id = 1  # noqa: A003
    name: str = "user"
    description: str = "normal user"

    @factory.post_generation
    def users(self, create, extracted, **kwargs):  # noqa: ARG002
        if not create:
            return
        if extracted:
            self.users.append(extracted)


class UserFactory(SQLAlchemyModelFactory):
    class Meta(CommonMeta):
        model = UserDBModel

    id = factory.Sequence(lambda n: n + 1)  # noqa: A003
    email = factory.Sequence(lambda n: f"user{n + 1}@domain.com")
    password = factory.Faker("password")
    fs_uniquifier = factory.LazyFunction(lambda: str(uuid.uuid4()))

    @factory.post_generation
    def ads(self, create, extracted, **kwargs):  # noqa: ARG002
        if not create:
            return
        if extracted:
            self.ads.append(extracted)

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):  # noqa: ARG002
        if not create:
            return
        if extracted:
            self.comments.append(extracted)


class AdFactory(SQLAlchemyModelFactory):
    class Meta(CommonMeta):
        model = AdDBModel

    id = factory.Sequence(lambda n: n + 1)  # noqa: A003
    content = factory.Sequence(lambda n: f"ad {n + 1}")

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):  # noqa: ARG002
        if not create:
            return
        if extracted:
            self.comments.append(extracted)


class CommentFactory(SQLAlchemyModelFactory):
    class Meta(CommonMeta):
        model = CommentDBModel

    id = factory.Sequence(lambda n: n + 1)  # noqa: A003
    content = factory.Sequence(lambda n: f"comment {n + 1}")
