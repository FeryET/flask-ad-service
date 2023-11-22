from collections.abc import Callable
from typing import Literal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from flask_ad_service.model import RoleDBModel, UserDBModel


def test_create_role_model_passes(
    db_test_session: Session, created_role: RoleDBModel
) -> None:
    queried = db_test_session.execute(
        select(RoleDBModel).filter_by(id=created_role.id)
    ).scalar_one()
    assert queried.id == created_role.id and created_role.id == 1
    assert queried.name == created_role.name and created_role.name == "user"
    assert (
        queried.description == created_role.description
        and created_role.description == "user role"
    )


@pytest.mark.parametrize("user_id", [1, 2])
def test_create_user_model_passes(
    db_test_session: Session,
    user_maker: Callable[[int], UserDBModel],
    user_id: Literal[1, 2],
) -> None:
    created_user = user_maker(user_id)
    queried = db_test_session.execute(
        select(UserDBModel).filter_by(id=created_user.id)
    ).scalar_one()
    assert queried.id == created_user.id
    assert queried.email == f"{created_user.id}@domain.com"
    assert queried.password == "123456"
    assert queried.fs_uniquifier == f"fs_uniquifier_{created_user.id}"
    assert queried.roles[0].name == "user"
    assert queried.roles[0].description == "user role"
    assert queried.ads == []
    assert queried.comments == []
