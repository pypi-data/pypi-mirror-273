from devtools.exc import DevtoolsError


class FilterError(DevtoolsError):
    """Base Error for all filter related exceptions"""


class FieldNotFound(FilterError, AttributeError):
    def __init__(self, name: str, field: str) -> None:
        super().__init__(f"type {name} has no {field} attribute")
