from typing import Literal

import pytest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from flask_ad_service.crud import crud_ad
from flask_ad_service.crud.common.exceptions import CrudItemNotFoundError
from flask_ad_service.crud.conditions import is_deleted
from flask_ad_service.model import AdDBModel, UserDBModel
from tests.faker.factories import AdFactory

pytestmark: pytest.MarkDecorator = pytest.mark.usefixtures(
    "_app_ctx", "db_test_session", "_populate_db"
)


@pytest.mark.parametrize("user", [1], indirect=True)
def test_ad_get_ad_by_id_returns_correct_value_and_type(
    database: SQLAlchemy, user: UserDBModel, non_existant_ad_id: Literal[10000]
) -> None:
    ad = AdFactory.create(author_id=user.id)
    q = crud_ad.get_ad_by_id(database, ad.id)
    assert ad == q
    assert isinstance(q, AdDBModel)

    # Should return none if the id is not found
    q = crud_ad.get_ad_by_id(database, non_existant_ad_id)
    assert q is None


@pytest.mark.parametrize("user", [1], indirect=True)
def test_ad_create_pass(database: SQLAlchemy, user: UserDBModel) -> None:
    ad, exc = crud_ad.create_ad(
        database,
        user.id,
        "created ad",
    )
    assert exc is None
    assert ad is not None
    assert isinstance(ad, AdDBModel)
    database.session.refresh(user)
    assert user.ads is not None
    assert user.ads[-1].id == ad.id


def test_crud_ad_create_ad_fail_for_user_that_does_not_exist(
    database: SQLAlchemy, non_existant_user_id: Literal[1000]
) -> None:
    with pytest.raises(IntegrityError):
        ad, exc = crud_ad.create_ad(
            database,
            non_existant_user_id,
            "created ad",
        )


@pytest.mark.parametrize("user", [1], indirect=True)
def test_crud_ad_delete_pass(database: SQLAlchemy, user: UserDBModel) -> None:
    ad = AdFactory.create(author_id=user.id)
    returned_ad, exc = crud_ad.delete_ad(database, ad.id)
    assert returned_ad is not None
    assert exc is None
    assert is_deleted(returned_ad)
    database.session.refresh(ad, attribute_names=["is_deleted"])
    assert ad == returned_ad


@pytest.mark.parametrize("user", [1], indirect=True)
def test_crud_ad_delete_returns_not_found_error(
    database: SQLAlchemy, user: UserDBModel, non_existant_ad_id: Literal[10000]
) -> None:
    returned_ad, exc = crud_ad.delete_ad(database, non_existant_ad_id)
    assert returned_ad is None
    assert exc is not None
    assert isinstance(exc, CrudItemNotFoundError)
