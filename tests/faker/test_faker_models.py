from collections.abc import Generator
from typing import Any

import pytest
from sqlalchemy.orm import Session

from flask_ad_service.model import RoleDBModel, UserDBModel
from tests.faker.factories import (
    AdFactory,
    CommentFactory,
    RoleFactory,
    UserFactory,
)

pytestmark = pytest.mark.usefixtures("_app_ctx", "db_test_session")


@pytest.fixture(scope="module")
def role(_app_ctx: None, db_test_session: Session) -> Generator[RoleDBModel, Any, None]:
    return RoleFactory.create()


@pytest.fixture(scope="module")
def users(
    _app_ctx: None,
    db_test_session: Session,
    role: RoleDBModel,
) -> Generator[list[UserDBModel], Any, None]:
    return UserFactory.create_batch(size=2, roles=[role])  # type: ignore


@pytest.fixture(scope="module")
def first_user(users: list[UserDBModel]) -> UserDBModel:
    return users[0]


@pytest.fixture(scope="module")
def second_user(users: list[UserDBModel]) -> UserDBModel:
    return users[1]


def test_role_factory_generating_roles(
    role: RoleDBModel,
) -> None:
    assert role.id == 1
    assert role.name == "user"
    assert role.description == "normal user"


def test_user_factory_generating_users(users: list[UserDBModel], role: RoleDBModel):
    for idx, u in enumerate(users, start=1):
        assert u.id == idx
        assert u.email == f"user{idx}@domain.com"


def test_user_factory_updates_role_factory(users: list[UserDBModel], role: RoleDBModel):
    assert role.users == users


def test_ad_factory_generates_ads_and_updates_users_ads(
    second_user: UserDBModel,
    db_test_session: Session,
) -> None:
    first_ad = AdFactory.create(author_id=second_user.id)
    assert first_ad.id == 1
    assert first_ad.author_id == second_user.id
    assert second_user.ads is not None
    assert second_user.ads[0].id == first_ad.id

    second_ad = AdFactory.create(author_id=second_user.id)
    assert second_ad.id == 2
    assert second_ad.author_id == second_user.id
    assert len(second_user.ads) == 2
    assert second_user.ads[1].id == second_ad.id


def test_comment_factory_generates_comments_and_updates_ads_comments(
    first_user: UserDBModel, second_user: UserDBModel
):
    ad = AdFactory.create(id=0, author_id=second_user.id)
    comment = CommentFactory.create(ad_id=ad.id, author_id=first_user.id)

    assert comment.id == 1
    assert comment.ad_id == ad.id
    assert ad.comments is not None
    assert ad.comments[0].id == comment.id
    assert ad.comments[0].ad_id == ad.id

    comment = CommentFactory.create(ad_id=ad.id, author_id=second_user.id)

    assert comment.id == 2
    assert comment.ad_id == ad.id
    assert len(ad.comments) == 2
    assert ad.comments[1].id == comment.id
    assert ad.comments[1].ad_id == ad.id


def test_comment_factory_generates_comments_and_updates_user_comments(
    role: RoleDBModel, first_user: UserDBModel, second_user: UserDBModel
):
    ad = AdFactory.create(author_id=first_user.id)
    user = UserFactory.create(roles=[role])
    comment = CommentFactory.create(ad_id=ad.id, author_id=user.id)

    assert comment.author_id == user.id
    assert user.comments is not None
    assert user.comments[0].id == comment.id
    assert user.comments[0].ad_id == ad.id
    assert user.comments[0].author_id == user.id

    ad = AdFactory.create(author_id=second_user.id)
    comment = CommentFactory.create(ad_id=ad.id, author_id=user.id)

    assert comment.author_id == user.id
    assert len(user.comments) == 2
    assert user.comments[1].id == comment.id
    assert user.comments[1].ad_id == ad.id
    assert user.comments[1].author_id == user.id
