from typing import Literal, cast

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from flask_ad_service.model import RoleDBModel, UserDBModel
from tests.faker.factories import AdFactory, CommentFactory, RoleFactory, UserFactory

pytestmark: pytest.MarkDecorator = pytest.mark.usefixtures(
    "_app_ctx", "db_test_session", "_populate_db"
)


@pytest.fixture(scope="module")
def _populate_db(
    _app_ctx,
    db_test_session: Session,
):
    role = RoleFactory.create()
    users = cast(list[UserDBModel], UserFactory.create_batch(size=5, roles=[role]))

    first_user, second_user, third_user = users[0], users[1], users[2]

    # populate ads
    ## first user gets 1 ad
    ad_by_first_user = AdFactory.create(author_id=first_user.id)
    ## second user 2 ads
    ads_by_second_user = AdFactory.create_batch(author_id=second_user.id, size=2)
    ## third user no ads

    # populate comments
    ## first user gets 2 comments
    CommentFactory.create(author_id=first_user.id, ad_id=ads_by_second_user[0].id)
    CommentFactory.create(author_id=first_user.id, ad_id=ads_by_second_user[1].id)
    ## second user no comments
    ## third user 1 comment
    CommentFactory.create(author_id=third_user.id, ad_id=ad_by_first_user.id)


@pytest.fixture(scope="module")
def role(_app_ctx, db_test_session) -> RoleDBModel:
    return RoleFactory.create(name="user", description="user role")


@pytest.fixture(scope="module")
def user(request, role) -> UserDBModel:
    return UserFactory.create(id=request.param, roles=[role])


@pytest.fixture()
def all_users(
    _app_ctx: None,
    db_test_session: Session,
    _populate_db,
) -> list[UserDBModel]:
    return list(db_test_session.execute(select(UserDBModel)).scalars().all())


@pytest.fixture()
def ads_count(_app_ctx: None, user: UserDBModel) -> Literal[1, 2, 0]:
    match user.id:
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 0
        case _:
            msg = "id has not been defined"
            raise ValueError(msg)


@pytest.fixture()
def comments_count(
    _app_ctx: None,
    user: UserDBModel,
) -> Literal[2, 0, 1]:
    match user.id:
        case 1:
            return 2
        case 2:
            return 0
        case 3:
            return 1
        case _:
            msg = "id has not been defined"
            raise ValueError(msg)
