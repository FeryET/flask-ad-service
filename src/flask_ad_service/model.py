from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_ad_service.database import db


class RoleUserDBModel(db.Model):
    __tablename__ = "users_roles_table"
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles_table.id"))


class RoleDBModel(db.Model):
    __tablename__ = "roles_table"
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    users: Mapped[list["UserDBModel"]] = relationship(
        secondary=RoleUserDBModel.__tablename__, back_populates="roles"
    )


class UserDBModel(db.Model):
    __tablename__ = "users_table"
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fs_uniquifier: Mapped[str] = mapped_column(unique=True, nullable=False)

    active: Mapped[bool] = mapped_column(default=True)
    roles: Mapped[list[RoleDBModel]] = relationship(
        secondary=RoleUserDBModel.__tablename__, back_populates="users"
    )

    # Relations
    ads: Mapped[list["AdDBModel"] | None] = relationship()
    comments: Mapped[list["CommentDBModel"] | None] = relationship()


class AdDBModel(db.Model):
    __tablename__ = "ads_table"
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    content: Mapped[str] = mapped_column(String(256))
    creation_at: Mapped[datetime] = mapped_column(server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)

    # Relations
    author_id: Mapped[int] = mapped_column(ForeignKey(UserDBModel.id), nullable=False)
    comments: Mapped[list["CommentDBModel"] | None] = relationship()


class CommentDBModel(db.Model):
    __tablename__ = "comments_table"
    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    content: Mapped[str] = mapped_column(String(256), nullable=False)
    submitted_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)

    # Relations
    author_id: Mapped["int"] = mapped_column(ForeignKey(UserDBModel.id), nullable=False)
    ad_id: Mapped[int] = mapped_column(ForeignKey(AdDBModel.id), nullable=False)


# class AdsCommentsDBModel(db.Model):
#     __tablename__ = "ads_comments_table"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     comment_id: Mapped[int] = mapped_column(
#         ForeignKey(CommentDBModel.id), nullable=False
#     )
#     ad_id: Mapped[int] = mapped_column(ForeignKey(AdDBModel.id), nullable=False)


# class UsersCommentsDBModel(db.Model):
#     __tablename__ = "users_comments_table"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     comment_id: Mapped[int] = mapped_column(
#         ForeignKey(CommentDBModel.id), nullable=False
#     )
#     comment_author_id: Mapped[int] = mapped_column(
#         ForeignKey(UserDBModel.id), nullable=False
#     )


# class UsersAdsDBModel(db.Model):
#     __tablename__ = "users_ads_table"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     ad_id: Mapped[int] = mapped_column(ForeignKey(AdDBModel.id), nullable=False)
#     ad_author_id: Mapped[int] = mapped_column(
#         ForeignKey(UserDBModel.id), nullable=False
#     )
