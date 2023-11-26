from dataclasses import dataclass

import pytest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

from flask_ad_service.crud.common.decorators import (
    commit_result_to_db,
    get_result_attribute_by_key,
    inject_model_by_id,
    insert_db_as_first_arg,
    pack_into_crud_result,
)
from flask_ad_service.crud.common.exceptions import CrudItemNotFoundError
from flask_ad_service.database import BaseModel


class TestModel(BaseModel):
    __tablename__ = "for_test_table"
    _id: Mapped[int] = mapped_column(primary_key=True)


class SampleTestFunctions:
    @commit_result_to_db  # type: ignore
    @staticmethod
    def _sample_func_for_commit_to_db_test(
        database: SQLAlchemy,  # noqa: ARG004
    ) -> tuple[TestModel, None]:
        return TestModel(), None

    @inject_model_by_id(TestModel)  # type: ignore
    @staticmethod
    def _sample_func_for_inject_model_by_id(
        database: SQLAlchemy,  # noqa: ARG004
        model: TestModel,
    ) -> tuple[TestModel, None]:
        return model, None


@pytest.fixture(scope="module", autouse=True)
def _prepare(database: SQLAlchemy):
    database.create_all()


def test_commit_result_to_db_return_value_correct(database: SQLAlchemy):
    v, e = SampleTestFunctions._sample_func_for_commit_to_db_test(database)
    assert v is not None
    assert v._id == 1


def test_commit_result_to_db_actually_commits(database: SQLAlchemy):
    v, e = SampleTestFunctions._sample_func_for_commit_to_db_test(database)
    q = database.session.get(TestModel, v._id)  # type: ignore
    assert q == v


def test_inject_model_by_id_returns_correct_values(database: SQLAlchemy):
    @inject_model_by_id(TestModel)  # type: ignore
    def func(database: SQLAlchemy, model: TestModel):
        return model, None

    v = TestModel()

    database.session.add(v)
    database.session.commit()

    assert v == func(database, v._id)[0]


def test_inject_model_by_id_returns_error_if_id_not_found(database: SQLAlchemy):
    v, e = SampleTestFunctions._sample_func_for_inject_model_by_id(database, 1000)
    assert isinstance(e, CrudItemNotFoundError)


def test_pack_into_result_works_correctly():
    @pack_into_crud_result
    def func():
        return 1

    v, e = func()
    assert v == 1
    assert e is None


def test_pack_into_result_does_not_catch_errors():
    @pack_into_crud_result
    def func(v):
        return v.some_field

    with pytest.raises(AttributeError):
        func(1)


def test_insert_db_as_first_arg_returns_the_same_value():
    db = SQLAlchemy()

    def func(a: int):
        return a

    assert func(1) == insert_db_as_first_arg(func)(db, 1)  # type: ignore


def test_get_result_attribute_by_key_returns_the_correct_value():
    @dataclass
    class A:
        a: int

    def func(a: int) -> tuple[A, None]:
        return A(a), None

    arg = 1
    simple_func_result = func(arg)
    decorated_func_result = get_result_attribute_by_key("a", int)(func)(arg)
    assert arg == simple_func_result[0].a == decorated_func_result[0]


def test_get_result_attribute_by_key_throws_error_if_attr_not_available():
    @dataclass
    class A:
        a: int

    @get_result_attribute_by_key("b", int)
    def func(a: int) -> tuple[A, None]:
        return A(a), None

    with pytest.raises(AttributeError):
        func(10)
