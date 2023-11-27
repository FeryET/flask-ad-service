from collections.abc import Callable
from typing import (
    Generic,
    ParamSpec,
    Protocol,
    TypeAlias,
    TypeVar,
)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped

from flask_ad_service.crud.common.exceptions import (
    CrudError,
    CrudItemNotFoundError,
    CrudUndefinedError,
)
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
Model_co = TypeVar(
    "Model_co",
    bound=AdDBModel | CommentDBModel | RoleDBModel | UserDBModel,
    covariant=True,
)

Params = ParamSpec("Params")
DecoratedParams = ParamSpec("DecoratedParams")
Ret_co = TypeVar("Ret_co", covariant=True)
Err_co = TypeVar("Err_co", bound=CrudError, covariant=True)


GeneralErr: TypeAlias = Err_co | CrudUndefinedError

Ret_inv = TypeVar("Ret_inv")
Err_inv = TypeVar("Err_inv", bound=CrudError)

Err_contra = TypeVar("Err_contra", bound=CrudError, contravariant=True)
Ret_contra = TypeVar("Ret_contra", contravariant=True)


Attr_co = TypeVar("Attr_co", covariant=True)


SuccessfulCrudResult: TypeAlias = tuple[Ret_inv, None]
FailedCrudResult: TypeAlias = tuple[None, Err_co]

CrudResult = SuccessfulCrudResult[Ret_inv] | FailedCrudResult[Err_co]


class FuncReturnsPackedResult(Generic[Params, Ret_co, Err_co], Protocol):
    def __call__(
        self, *args: Params.args, **kwds: Params.kwargs
    ) -> CrudResult[Ret_co, GeneralErr[Err_co]]:
        ...


class FuncHasDBAsFirstParameter(Generic[Params, Ret_co, Err_co], Protocol):
    def __call__(
        self,
        db: SQLAlchemy,
        *args: Params.args,
        **kwds: Params.kwargs,
    ) -> CrudResult[Ret_co, GeneralErr[Err_co]]:
        ...


class FuncHasIdAsSecondParameter(Generic[Params, Ret_co, Err_co], Protocol):
    def __call__(
        self,
        db: SQLAlchemy,
        id: int,  # noqa: A002
        *args: Params.args,
        **kwargs: Params.kwargs,
    ) -> CrudResult[Ret_co, GeneralErr[Err_co] | CrudItemNotFoundError]:
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
    ) -> CrudResult[Ret_co, GeneralErr[Err_co]]:
        ...


class FuncReturnsAttributeOfResultValue(Generic[Params, Attr_co, Err_co], Protocol):
    def __call__(
        self, *args: Params.args, **kwds: Params.kwargs
    ) -> CrudResult[Attr_co, GeneralErr[Err_co]]:
        ...


class DecoratedToInsertDBAsFirstParameter(Protocol):
    def __call__(
        self, func: Callable[Params, CrudResult[Ret_inv, GeneralErr[Err_inv]]]
    ) -> FuncHasDBAsFirstParameter[Params, Ret_inv, Err_inv]:
        ...


class DecoratedToInsertIdAsSecondParameterToGetModel(Generic[Model_co], Protocol):
    def __call__(
        self,
        func: FuncHasModelAsSecondParameter[Params, Model_co, Ret_inv, Err_inv],
    ) -> FuncHasIdAsSecondParameter[Params, Ret_inv, Err_inv | CrudItemNotFoundError]:
        ...


class DecoratedToReturnResultPacker(Generic[Err_co], Protocol):
    def __call__(
        self, func: Callable[Params, Ret_inv]
    ) -> FuncReturnsPackedResult[Params, Ret_inv, Err_co]:
        ...


class DecoratedToReturnAttributeOfResultValue(Generic[Attr_co], Protocol):
    def __call__(
        self, func: FuncReturnsPackedResult[Params, Ret_contra, Err_inv]
    ) -> FuncReturnsAttributeOfResultValue[Params, Attr_co, Err_inv]:
        ...


class HasAuthorProtocol(Protocol):
    author_id: Mapped[int]


class DeletableProtocol(Protocol):
    is_deleted: Mapped[bool]
