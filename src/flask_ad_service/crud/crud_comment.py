from flask_sqlalchemy import SQLAlchemy

from flask_ad_service.crud.common.decorators import (
    commit_result_to_db,
    inject_model_by_id,
    insert_db_as_first_arg,
    pack_into_crud_result,
)
from flask_ad_service.crud.common.functions import (
    generic_get_by_id,
)
from flask_ad_service.model import CommentDBModel


def get_comment_by_id(db: SQLAlchemy, comment_id: int) -> CommentDBModel | None:
    return generic_get_by_id(db, CommentDBModel, comment_id)


@commit_result_to_db
@insert_db_as_first_arg
@pack_into_crud_result
def create_comment(author_id: int, ad_id: int, comment_content: str) -> CommentDBModel:
    return CommentDBModel(author_id=author_id, ad_id=ad_id, content=comment_content)  # type: ignore


@commit_result_to_db
@inject_model_by_id(CommentDBModel)
@insert_db_as_first_arg
@pack_into_crud_result
def delete_comment(model: CommentDBModel) -> CommentDBModel:
    model.is_deleted = True
    return model
