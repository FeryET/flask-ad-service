import pytest
from flask_sqlalchemy import SQLAlchemy

from flask_ad_service.crud import crud_user
from flask_ad_service.model import UserDBModel

pytestmark: pytest.MarkDecorator = pytest.mark.usefixtures(
    "_app_ctx", "db_test_session", "_populate_db"
)


@pytest.mark.parametrize("user", [1, 2, 3], indirect=True)
def test_get_user_by_id_instance_matches_the_user(
    database: SQLAlchemy, user: UserDBModel
) -> None:
    assert user == crud_user.get_user_by_id(database, user.id)


@pytest.mark.parametrize("user", [1, 2, 3], indirect=True)
def test_get_user_ads_matches_the_user_ads(user: UserDBModel, ads_count: int) -> None:
    fetched_ads = crud_user.get_user_ads(user)
    assert fetched_ads == user.ads
    assert len(fetched_ads) == ads_count


@pytest.mark.parametrize("user", [1, 2, 3], indirect=True)
def test_get_user_comments_matches_the_user_comments(
    database: SQLAlchemy, user: UserDBModel, comments_count: int
) -> None:
    fetched_comments = crud_user.get_user_comments(user)
    assert fetched_comments == user.comments
    assert len(fetched_comments) == comments_count
