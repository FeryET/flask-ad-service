from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from flask_ad_service.model import AdDBModel, CommentDBModel, UserDBModel


def test_creating_comment_db_model_pass(
    db_test_session: Session,
    users: list[UserDBModel],
    ads: list[AdDBModel],
    comment_maker: Callable[[int, int], CommentDBModel],
) -> None:
    c = comment_maker(users[0].id, ads[0].id)
    db_test_session.delete(c)
    db_test_session.commit()


def test_created_comment_db_model_matches_queried(
    db_test_session: Session, comments: list[CommentDBModel]
):
    queried_comments = (
        db_test_session.execute(
            select(CommentDBModel).filter(
                CommentDBModel.id.in_([c.id for c in comments])
            )
        )
        .scalars()
        .all()
    )
    for q, c in zip(queried_comments, comments, strict=True):
        assert q.id == c.id
        assert q.author_id == c.author_id
        assert q.ad_id == c.ad_id


def test_comment_db_model_relationship_with_ad_db_model(
    db_test_session: Session, ads: list[AdDBModel], comments: list[CommentDBModel]
):
    query = select(AdDBModel, CommentDBModel).where(
        CommentDBModel.ad_id == AdDBModel.id,
    )
    for curr_ad, curr_comment in db_test_session.execute(query).tuples().all():
        assert curr_comment in comments
        if curr_ad.id == curr_comment.ad_id:
            assert curr_ad.comments is not None
            assert curr_comment in curr_ad.comments
        elif curr_ad.comments is not None:
            assert curr_comment not in curr_ad.comments


def test_comment_db_model_relationship_with_user_db_model(
    db_test_session: Session, users: list[UserDBModel], comments: list[CommentDBModel]
):
    query = select(UserDBModel, CommentDBModel).where(
        CommentDBModel.author_id == UserDBModel.id,
    )
    for curr_user, curr_comment in db_test_session.execute(query).tuples().all():
        assert curr_comment in comments
        if curr_user.id == curr_comment.author_id:
            assert curr_user.comments is not None
            assert curr_comment in curr_user.comments
        elif curr_user.comments is not None:
            assert curr_comment not in curr_user.comments
