from typing import TYPE_CHECKING, Literal

import pytest
from flask_sqlalchemy import SQLAlchemy

from flask_ad_service.crud import crud_comment
from flask_ad_service.crud.common.exceptions import CrudItemNotFoundError
from flask_ad_service.model import CommentDBModel, UserDBModel
from tests.faker.factories import AdFactory, CommentFactory, UserFactory

if TYPE_CHECKING:
    from flask_ad_service.model import AdDBModel


@pytest.mark.parametrize("user", [1], indirect=True)
def test_create_comment_pass(database: SQLAlchemy, user: UserDBModel):
    new_user: UserDBModel = UserFactory.create(roles=user.roles)
    ad: "AdDBModel" = AdFactory.create(author_id=user.id)
    c, exc = crud_comment.create_comment(
        db=database, author_id=new_user.id, ad_id=ad.id, comment_content="comment"
    )
    assert c is not None
    assert isinstance(c, CommentDBModel)
    assert exc is None
    assert ad.comments is not None
    assert c in ad.comments


@pytest.mark.parametrize("user", [1], indirect=True)
def test_delete_comment_pass(database: SQLAlchemy, user: UserDBModel) -> None:
    ad: AdDBModel = AdFactory.create(author_id=user.id)
    comment = CommentFactory.create(ad_id=ad.id, author_id=user.id)
    c, exc = crud_comment.delete_comment(database, comment.id)
    assert c is not None
    assert exc is None
    assert comment == c
    assert c.is_deleted


@pytest.mark.parametrize("user", [1], indirect=True)
def test_delete_comment_returns_not_found_error(
    database: SQLAlchemy, user: UserDBModel, non_existant_comment_id: Literal[100000]
) -> None:
    c, exc = crud_comment.delete_comment(database, non_existant_comment_id)
    assert c is None
    assert exc is not None
    assert isinstance(exc, CrudItemNotFoundError)
