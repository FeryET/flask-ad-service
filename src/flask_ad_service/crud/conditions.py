from typing import TYPE_CHECKING

from flask_ad_service.crud.crud_ad import get_ad_comments

if TYPE_CHECKING:
    from flask_ad_service.crud._crud_typing import DeletableProtocol, HasAuthorProtocol
    from flask_ad_service.model import AdDBModel, CommentDBModel, UserDBModel


def is_user_the_item_author(user: "UserDBModel", item: "HasAuthorProtocol") -> bool:
    return item.author_id == user.id


def can_user_comment_on_ad(ad: "AdDBModel", user: "UserDBModel") -> bool:
    return not any(is_user_the_item_author(user, c) for c in get_ad_comments(ad))


def was_comment_posted_for_ad(ad: "AdDBModel", comment: "CommentDBModel") -> bool:
    return any(c.id == comment.id for c in get_ad_comments(ad))


def is_deleted(item: "DeletableProtocol") -> bool:
    return item.is_deleted
