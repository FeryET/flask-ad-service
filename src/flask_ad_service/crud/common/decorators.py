from functools import wraps
from typing import TYPE_CHECKING

from flask_ad_service.crud.common.exceptions import (
    CrudItemNotFoundError,
    CrudUndefinedError,
)
from flask_ad_service.crud.common.functions import generic_get_by_id

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import ParamSpec, TypeAlias, TypeVar

    from flask_sqlalchemy import SQLAlchemy

    from flask_ad_service.crud._crud_typing import (
        CrudResult,
        DecoratedToInsertIdAsSecondParameterToGetModel,
        DecoratedToReturnAttributeOfResultValue,
        FuncHasDBAsFirstParameter,
        FuncHasIdAsSecondParameter,
        FuncHasModelAsSecondParameter,
        FuncReturnsPackedResult,
        Model,
        SuccessfulCrudResult,
    )
    from flask_ad_service.crud.common.exceptions import (
        CrudError,
    )

    CrudFuncParams = ParamSpec("CrudFuncParams")
    CrudFuncRet = TypeVar("CrudFuncRet")
    CrudFuncErr = TypeVar("CrudFuncErr", bound=CrudError)
    CrudGeneralErr: TypeAlias = CrudFuncErr | CrudUndefinedError
    CrudFuncResultAttr = TypeVar("CrudFuncResultAttr")


def pack_into_crud_result(
    func: "Callable[CrudFuncParams, CrudFuncRet]"
) -> "Callable[CrudFuncParams, SuccessfulCrudResult[CrudFuncRet]]":
    @wraps(func)
    def wrapper(
        *args: "CrudFuncParams.args", **kwargs: "CrudFuncParams.kwargs"
    ) -> "SuccessfulCrudResult[CrudFuncRet]":
        return func(*args, **kwargs), None

    return wrapper


def get_result_attribute_by_key(
    attr_key: str,
    _attr_type: "type[CrudFuncResultAttr]",
    /,
) -> "DecoratedToReturnAttributeOfResultValue[CrudFuncParams, CrudFuncRet, CrudFuncResultAttr, CrudFuncErr]":  # noqa: E501
    def inner(
        func: "FuncReturnsPackedResult[CrudFuncParams, CrudFuncRet, CrudFuncErr]",
    ) -> "FuncReturnsPackedResult[CrudFuncParams, CrudFuncResultAttr, CrudFuncErr]":
        @wraps(func)
        def wrapper(
            *args: "CrudFuncParams.args", **kwargs: "CrudFuncParams.kwargs"
        ) -> "CrudResult[CrudFuncResultAttr, CrudGeneralErr[CrudFuncErr]]":
            v, e = func(*args, **kwargs)
            if e is not None:
                return None, e
            if v is not None:
                return getattr(v, attr_key), e
            else:
                return None, CrudUndefinedError()

        return wrapper

    return inner


def commit_result_to_db(
    func: "FuncHasDBAsFirstParameter[CrudFuncParams, CrudFuncRet, CrudFuncErr]"
) -> "FuncHasDBAsFirstParameter[CrudFuncParams, CrudFuncRet, CrudFuncErr]":
    @wraps(func)
    def wrapper(
        db: "SQLAlchemy",
        *args: "CrudFuncParams.args",
        **kwargs: "CrudFuncParams.kwargs",
    ) -> "CrudResult[CrudFuncRet, CrudGeneralErr[CrudFuncErr]]":
        v, e = func(db, *args, **kwargs)
        if e is not None:
            return None, e
        if v is not None:
            db.session.add(v)
            db.session.commit()
            return v, None
        else:
            return None, CrudUndefinedError()

    return wrapper


def inject_model_by_id(
    model_class: "type[Model]", /
) -> "DecoratedToInsertIdAsSecondParameterToGetModel[CrudFuncParams, Model, CrudFuncRet, CrudFuncErr]":  # noqa: E501
    def inner(
        func: "FuncHasModelAsSecondParameter[CrudFuncParams, Model, CrudFuncRet, CrudFuncErr]",  # noqa: E501
    ) -> "FuncHasIdAsSecondParameter[CrudFuncParams, CrudFuncRet, CrudFuncErr | CrudItemNotFoundError]":  # noqa: E501
        @wraps(func)
        def wrapper(
            db: "SQLAlchemy",
            id: "int",  # noqa: A002
            *args: "CrudFuncParams.args",
            **kwargs: "CrudFuncParams.kwargs",
        ) -> "CrudResult[CrudFuncRet, CrudGeneralErr[CrudFuncErr] | CrudItemNotFoundError]":  # noqa: E501
            v = generic_get_by_id(db, model_class, id)
            if v is None:
                return None, CrudItemNotFoundError()
            else:
                return func(db, v, *args, **kwargs)

        return wrapper

    return inner


def insert_db_as_first_arg(
    func: "FuncReturnsPackedResult[CrudFuncParams, CrudFuncRet, CrudFuncErr]"
) -> "FuncHasDBAsFirstParameter[CrudFuncParams, CrudFuncRet, CrudFuncErr]":
    def wrapper(
        db: "SQLAlchemy",  # noqa: ARG001
        *args: "CrudFuncParams.args",
        **kwargs: "CrudFuncParams.kwargs",
    ) -> "CrudResult[CrudFuncRet, CrudGeneralErr[CrudFuncErr]]":
        return func(*args, **kwargs)

    return wrapper
