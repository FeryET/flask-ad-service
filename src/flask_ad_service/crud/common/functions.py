from flask_sqlalchemy import SQLAlchemy

from flask_ad_service.crud._crud_typing import (
    Model,
)


def generic_get_by_id(db: SQLAlchemy, entity: type[Model], id: int) -> Model | None:  # noqa: A002
    return db.session.get(entity, id)
