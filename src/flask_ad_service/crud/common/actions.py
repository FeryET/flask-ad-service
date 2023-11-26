from abc import ABC
from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy


@dataclass(frozen=True, kw_only=True)
class CrudRequest(ABC):
    db: SQLAlchemy


@dataclass(frozen=True, kw_only=True)
class ByIDCrudRequest(CrudRequest):
    id: int  # noqa: A003


@dataclass(frozen=True, kw_only=True)
class AdCreationRequest(CrudRequest):
    user_id: int
    content: str


@dataclass(frozen=True, kw_only=True)
class AdUpdateRequest(ByIDCrudRequest):
    content: str


@dataclass(frozen=True, kw_only=True)
class CommentCreationRequest(CrudRequest):
    author_id: int
    ad_id: int
    content: str


@dataclass(frozen=True, kw_only=True)
class CommentUpdateRequest(ByIDCrudRequest):
    content: str
