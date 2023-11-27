from flask_sqlalchemy import SQLAlchemy

from flask_ad_service.crud.common.decorators import (
    commit_result_to_db,
    inject_model_by_id,
    insert_db_as_first_arg,
    pack_into_crud_result,
)
from flask_ad_service.crud.common.functions import generic_get_by_id
from flask_ad_service.model import AdDBModel, CommentDBModel


def get_ad_by_id(db: SQLAlchemy, id: int) -> AdDBModel | None:  # noqa: A002
    return generic_get_by_id(db, AdDBModel, id)


@commit_result_to_db
@insert_db_as_first_arg
@pack_into_crud_result
def create_ad(author_id: int, content: str) -> AdDBModel:
    return AdDBModel(author_id=author_id, content=content)  # type: ignore


@commit_result_to_db
@inject_model_by_id(AdDBModel)
@insert_db_as_first_arg
@pack_into_crud_result
def delete_ad(model: AdDBModel) -> AdDBModel:
    model.is_deleted = True
    return model


@commit_result_to_db
@inject_model_by_id(AdDBModel)
@insert_db_as_first_arg
@pack_into_crud_result
def update_ad(model: AdDBModel, content: str) -> AdDBModel:
    model.content = content
    return model


def get_ad_comments(model: AdDBModel) -> list[CommentDBModel]:
    return [] if model.comments is None else model.comments
