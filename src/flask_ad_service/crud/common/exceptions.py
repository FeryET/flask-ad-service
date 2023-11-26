from dataclasses import dataclass


@dataclass(frozen=True)
class CrudError(Exception):
    message: str = ""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"


class CrudUndefinedError(CrudError):
    pass


class CrudCommitError(CrudError):
    pass


class CrudItemNotFoundError(CrudError):
    pass


class CrudActionNotPossibleError(CrudError):
    pass
