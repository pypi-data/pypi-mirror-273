from typing import Any, Generator, Sequence, Union

from devtools.attrs import define, fields
from devtools.attrs.field import Field
from devtools.attrs.utils.typedef import MISSING as NOTHING
from devtools.config import MISSING
from devtools.config.adapter.interface import FieldResolverStrategy


@define
class DevtoolsAttrsResolverStrategy(FieldResolverStrategy[Field]):
    field: Field

    def cast(self) -> type:
        return self.field.declared_type

    def names(self) -> Sequence[str]:
        return self.field.name, self.field.alias

    def init_name(self) -> str:
        return self.field.alias or self.field.name

    def default(self) -> Union[Any, type[MISSING]]:
        default = self.field.default
        if default is NOTHING:
            return MISSING
        return default() if self.field.has_default_factory else default

    @staticmethod
    def iterfield(config_class: type) -> Generator[Field, Any, Any]:
        yield from fields(config_class).values()
