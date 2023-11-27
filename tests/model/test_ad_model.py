from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from flask_ad_service.model import AdDBModel, UserDBModel


def test_creating_ad_db_model_pass(
    db_test_session: Session,
    users: list[UserDBModel],
    ad_maker: Callable[[int], AdDBModel],
) -> None:
    ad = ad_maker(users[0].id)
    assert ad.author_id == users[0].id
    assert ad.is_deleted is False
    db_test_session.delete(ad)
    db_test_session.commit()


def test_ad_db_model_creation_matches_with_queried(
    db_test_session: Session,
    ads: list[AdDBModel],
) -> None:
    queried_ads = (
        db_test_session.execute(
            select(AdDBModel).filter(AdDBModel.id.in_([a.id for a in ads]))
        )
        .scalars()
        .all()
    )
    for q, a in zip(queried_ads, ads, strict=True):
        assert q.id == a.id
        assert q.content == a.content
        assert q.is_deleted == a.is_deleted
        assert q.author_id == a.author_id
        assert q.comments == a.comments


def test_ad_db_model_relationship_with_user_pass(
    db_test_session: Session,
    users: list[UserDBModel],
    ads: list[AdDBModel],
) -> None:
    for curr_ad, curr_user in (
        db_test_session.execute(
            select(AdDBModel, UserDBModel).where(AdDBModel.author_id == UserDBModel.id)
        )
        .tuples()
        .all()
    ):
        assert curr_ad in ads
        if curr_ad.author_id == curr_user.id:
            assert curr_user.ads is not None
            assert curr_ad in curr_user.ads
        elif curr_user.ads is not None:
            assert curr_ad not in curr_user.ads
