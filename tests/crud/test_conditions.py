from dataclasses import dataclass

import pytest
from sqlalchemy.orm import Session

from flask_ad_service.crud._crud_typing import DeletableProtocol
from flask_ad_service.crud.conditions import (
    can_user_comment_on_ad,
    is_deleted,
    is_user_the_item_author,
    was_comment_posted_for_ad,
)
from flask_ad_service.model import AdDBModel, UserDBModel
from tests.faker.factories import AdFactory, CommentFactory, RoleFactory, UserFactory


def test_is_deleted():
    @dataclass
    class Deletable(DeletableProtocol):
        is_deleted: bool

    assert is_deleted(Deletable(True))
    assert not is_deleted(Deletable(False))


@pytest.mark.parametrize("user", [1], indirect=True)
@pytest.mark.usefixtures("db_test_session")
def test_is_author_the_user(user: UserDBModel) -> None:
    assert is_user_the_item_author(user, AdDBModel(author_id=user.id, content="ad"))  # type: ignore
    assert not is_user_the_item_author(user, AdDBModel(author_id=1_000, content="ad"))  # type: ignore


@pytest.mark.parametrize("user", [1], indirect=True)
def test_is_ad_parent_of_comment(
    db_test_session: Session,
    user: UserDBModel,
):
    # Test when should be the comment's parent
    ad_poster = UserFactory.create(roles=user.roles)
    ad = AdFactory.create(author_id=ad_poster.id)
    assert was_comment_posted_for_ad(
        ad,
        CommentFactory.create(author_id=user.id, ad_id=ad.id),  # type: ignore
    )
    new_user = UserFactory.build()
    assert not was_comment_posted_for_ad(
        ad,
        CommentFactory.build(author_id=new_user.id, ad_id=ad.id),  # type: ignore
    )


@pytest.mark.parametrize("user", [1], indirect=True)
def test_can_user_comment_on_ad(db_test_session: Session, user: UserDBModel):
    role = RoleFactory.create()
    new_user = UserFactory.create(roles=[role])

    ad = AdFactory.create(author_id=user.id)

    assert can_user_comment_on_ad(ad, new_user) is True

    CommentFactory.create(author_id=new_user.id, ad_id=ad.id)

    assert can_user_comment_on_ad(ad, new_user) is False
