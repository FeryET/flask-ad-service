from collections.abc import Callable
from typing import (
    Generic,
    ParamSpec,
    Protocol,
    TypeVar,
)

from flask_sqlalchemy import SQLAlchemy

from flask_ad_service.crud.structs import (
    CrudResult,
)
from flask_ad_service.exceptions import CrudError
from flask_ad_service.model import (
    AdDBModel,
    CommentDBModel,
    RoleDBModel,
    UserDBModel,
)

Model = TypeVar(
    "Model",
    bound=AdDBModel | CommentDBModel | RoleDBModel | UserDBModel,
)

Model_contra = TypeVar(
    "Model_contra",
    bound=AdDBModel | CommentDBModel | RoleDBModel | UserDBModel,
    contravariant=True,
)

Params = ParamSpec("Params")
DecoratedParams = ParamSpec("DecoratedParams")
Ret_co = TypeVar("Ret_co", covariant=True)
Err_co = TypeVar("Err_co", bound=CrudError, covariant=True)

Ret_inv = TypeVar("Ret_inv")
Err_inv = TypeVar("Err_inv", bound=CrudError)

Err_contra = TypeVar("Err_contra", bound=CrudError, contravariant=True)
Ret_contra = TypeVar("Ret_contra", contravariant=True)


Attr_co = TypeVar("Attr_co", covariant=True)


class FuncReturnsPackedResult(Generic[Params, Ret_co, Err_co], Protocol):
    def __call__(
        self, *args: Params.args, **kwds: Params.kwargs
    ) -> CrudResult[Ret_co, Err_co]:
        ...


class FuncHasDBAsFirstParameter(Generic[Params, Ret_co, Err_co], Protocol):
    def __call__(
        self,
        db: SQLAlchemy,
        *args: Params.args,
        **kwds: Params.kwargs,
    ) -> CrudResult[Ret_co, Err_co]:
        ...


class FuncHasIdAsSecondParameter(Generic[Params, Ret_co, Err_co], Protocol):
    def __call__(
        self,
        db: SQLAlchemy,
        id: int,  # noqa: A002
        *args: Params.args,
        **kwargs: Params.kwargs,
    ) -> CrudResult[Ret_co, Err_co]:
        ...


class FuncHasModelAsSecondParameter(
    Generic[Params, Model_contra, Ret_co, Err_co],
    Protocol,
):
    def __call__(
        self,
        db: SQLAlchemy,
        model: Model_contra,
        *args: Params.args,
        **kwargs: Params.kwargs,
    ) -> CrudResult[Ret_co, Err_co]:
        ...


class FuncReturnsAttributeOfResultValue(Generic[Params, Attr_co, Err_co], Protocol):
    def __call__(
        self, *args: Params.args, **kwds: Params.kwargs
    ) -> CrudResult[Attr_co, Err_co]:
        ...


class InsertDBAsFirstParameterDecorator(Generic[Params, Ret_inv, Err_inv], Protocol):
    def __call__(
        self, func: Callable[Params, CrudResult[Ret_inv, Err_inv]]
    ) -> FuncHasDBAsFirstParameter[Params, Ret_inv, Err_inv]:
        ...


class InsertIdAsSecondParameterDecorator(Generic[Params, Ret_inv, Err_inv], Protocol):
    def __call__(
        self,
        func: FuncHasDBAsFirstParameter[Params, Ret_inv, Err_inv],
    ) -> FuncHasIdAsSecondParameter[Params, Ret_inv, Err_inv]:
        ...


class InsertModelAsSecondParameterDecorator(
    Generic[Params, Model_contra, Ret_inv], Protocol
):
    def __call__(
        self, func: FuncHasIdAsSecondParameter[Params, Ret_inv, Err_co]
    ) -> FuncHasModelAsSecondParameter[Params, Model_contra, Ret_inv, Err_co]:
        ...


class MakeFunctionResultPackerDecorator(Generic[Params, Ret_inv, Err_co], Protocol):
    def __call__(
        self, func: Callable[Params, Ret_inv]
    ) -> FuncReturnsPackedResult[Params, Ret_inv, Err_co]:
        ...


class MakeFunctionReturnAttributeOfResultValue(
    Generic[Params, Ret_contra, Attr_co, Err_inv], Protocol
):
    def __call__(
        self, func: FuncReturnsPackedResult[Params, Ret_contra, Err_inv]
    ) -> FuncReturnsAttributeOfResultValue[Params, type[Attr_co], Err_inv]:
        ...
