import sys


class DevtoolsError(Exception):
    ...


class InvalidCast(DevtoolsError):
    ...


class MissingName(DevtoolsError, KeyError):
    ...


class InvalidField(DevtoolsError, KeyError):
    ...


class CacheMiss(DevtoolsError, KeyError):
    ...


class MissingParams(DevtoolsError, NotImplementedError):
    ...


class InvalidPath(DevtoolsError, ValueError):
    ...


class InvalidParamValue(DevtoolsError, ValueError):
    ...


if sys.version_info < (3, 11):

    class ErrorGroup(DevtoolsError):
        exceptions: tuple[Exception, ...]

        def __init__(self, message: str, exceptions: Sequence[Exception]) -> None:
            self.message = message
            self.exceptions = tuple(exceptions)
            args = list(chain(item.args for item in exceptions))
            super().__init__(self.message, *args)

        def __str__(self) -> str:
            suffix = "" if len(self.exceptions) == 1 else "s"
            return f"{self.message} ({len(self.exceptions)} sub-exception{suffix})"

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self.message!r}, {self.exceptions!r})"

else:

    class ErrorGroup(DevtoolsError):
        ...


class FailedFileOperation(DevtoolsError):
    ...


class MergeConflict(DevtoolsError):
    ...
