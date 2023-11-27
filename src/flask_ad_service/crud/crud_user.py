from typing import cast

from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from flask_sqlalchemy import SQLAlchemy

from flask_ad_service.crud.common.decorators import (
    commit_result_to_db,
    get_result_attribute_by_key,
    insert_db_as_first_arg,
    pack_into_crud_result,
)
from flask_ad_service.crud.common.functions import generic_get_by_id
from flask_ad_service.model import AdDBModel, CommentDBModel, UserDBModel


def get_user_by_id(db: SQLAlchemy, user_id: int) -> UserDBModel | None:
    return generic_get_by_id(db, UserDBModel, user_id)


def get_user_comments(model: UserDBModel) -> list[CommentDBModel]:
    return [] if model.comments is None else model.comments


def get_user_ads(model: UserDBModel) -> list[AdDBModel]:
    return [] if model.ads is None else model.ads


@get_result_attribute_by_key("id", int)
@commit_result_to_db
@insert_db_as_first_arg
@pack_into_crud_result
def create_user(
    user_store: SQLAlchemyUserDatastore, email: str, password: str
) -> UserDBModel:
    return cast(
        UserDBModel,
        user_store.create_user(
            email=email,
            password=hash_password(password),
            role=["user"],  # TODO: hardcoded role
        ),
    )
