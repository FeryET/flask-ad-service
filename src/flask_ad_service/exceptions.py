from dataclasses import dataclass


@dataclass(frozen=True)
class CrudError(Exception):
    message: str = ""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"


# ------------------------------------------------------------------------------
# User Exceptions
# ------------------------------------------------------------------------------


class UserCreationError(CrudError):
    pass


class UserCommentFetchError(CrudError):
    pass


class UserAdsFetchError(CrudError):
    pass


# ------------------------------------------------------------------------------
# Ad Exceptions
# ------------------------------------------------------------------------------


class AdCommentsFetchError(CrudError):
    pass


class AdUserFetchError(CrudError):
    pass


class AdCreationError(CrudError):
    pass


class AdDeletionError(CrudError):
    pass


class AdUpdateError(CrudError):
    pass


# ------------------------------------------------------------------------------
# Comment Exceptions
# ------------------------------------------------------------------------------


class CommentFetchUserError(CrudError):
    pass


class CommentFetchAdError(CrudError):
    pass


class CommentDeletionError(CrudError):
    pass


class CommentCreationError(CrudError):
    pass
