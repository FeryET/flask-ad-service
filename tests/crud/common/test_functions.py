import pytest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

from flask_ad_service.crud.common.functions import generic_get_by_id
from flask_ad_service.database import db


class Item(db.Model):
    __tablename__ = "items_table"
    _id: Mapped[int] = mapped_column(primary_key=True)


@pytest.fixture(scope="module", autouse=True)
def _prepare(database: SQLAlchemy):
    database.create_all()


def test_generic_get_by_id_matches_created_item(database: SQLAlchemy) -> None:
    created_item = Item()
    database.session.add(created_item)
    database.session.commit()

    assert generic_get_by_id(database, Item, id=1) == created_item  # type: ignore


def test_generic_get_by_id_returns_none_for_not_found(database: SQLAlchemy) -> None:
    assert generic_get_by_id(database, Item, id=10_000) is None  # type: ignore
