from collections.abc import Callable

import pytest
from sqlalchemy.orm import Session

from flask_ad_service.model import AdDBModel, CommentDBModel, RoleDBModel, UserDBModel

pytestmark = pytest.mark.usefixtures("_app_ctx", "db_test_session")


@pytest.fixture(scope="module")
def created_role(
    _app_ctx: None, db_test_session: Session, request: pytest.FixtureRequest
) -> RoleDBModel:
    role = RoleDBModel(name="user", description="user role")  # type: ignore
    db_test_session.add(role)
    db_test_session.commit()
    return role


@pytest.fixture(scope="module")
def user_maker(
    _app_ctx: None,
    db_test_session: Session,
    created_role: RoleDBModel,
) -> Callable[[int], UserDBModel]:
    def maker(user_id: int) -> UserDBModel:
        user = UserDBModel(
            roles=[created_role],
            email=f"{user_id}@domain.com",
            password="123456",
            fs_uniquifier=f"fs_uniquifier_{user_id}",
        )  # type: ignore
        db_test_session.add(user)
        db_test_session.commit()
        return user

    return maker


@pytest.fixture(scope="module")
def ad_maker(
    _app_ctx: None,
    db_test_session: Session,
    request: pytest.FixtureRequest,
) -> Callable[[int], AdDBModel]:
    def maker(author_id: int) -> AdDBModel:
        ad = AdDBModel(author_id=author_id, content=f"ad by user {author_id}")  # type: ignore
        db_test_session.add(ad)
        db_test_session.commit()
        return ad

    return maker


@pytest.fixture(scope="module")
def comment_maker(
    _app_ctx: None, db_test_session: Session, request: pytest.FixtureRequest
) -> Callable[[int, int], CommentDBModel]:
    def maker(author_id: int, ad_id: int) -> CommentDBModel:
        comment = CommentDBModel(
            author_id=author_id,
            ad_id=ad_id,
            content=f"comment for ad {ad_id} by user {author_id}",
        )  # type: ignore
        db_test_session.add(comment)
        db_test_session.commit()
        return comment

    return maker


@pytest.fixture(scope="module")
def users(user_maker: Callable[[int], UserDBModel]):
    return [user_maker(user_id) for user_id in range(3)]


@pytest.fixture(scope="module")
def ads(ad_maker: Callable[[int], AdDBModel], users: list[UserDBModel]):
    return [ad_maker(user.id) for user in users]


@pytest.fixture(scope="module")
def comments(
    comment_maker: Callable[[int, int], CommentDBModel],
    ads: list[AdDBModel],
    users: list[UserDBModel],
):
    return [
        comment_maker(user.id, ad.id)
        for user in users
        for ad in ads
        if user.id != ad.author_id
    ]
