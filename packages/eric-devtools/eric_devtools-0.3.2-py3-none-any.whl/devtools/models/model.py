from typing import Any

from pydantic import BaseModel, ConfigDict, __version__

from devtools.lazyfields import lazy

pydantic_version = tuple(int(i) for i in __version__.split(".") if i.isdigit())

if pydantic_version < (2, 0, 0):
    raise ImportError("Unable to use .v2, install pydantic>=2.0.0", __version__)


from pydantic import BaseModel, ConfigDict

from devtools.utils import to_camel


class Model(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        from_attributes=True,
        ignored_types=(lazy,),
        alias_generator=to_camel,
    )

    def __setattr__(self, name: str, value: Any) -> None:
        if isinstance(getattr(type(self), name, None), lazy):
            object.__setattr__(self, name, value)
        else:
            return super().__setattr__(name, value)


class MutableModel(Model):
    model_config = ConfigDict(frozen=False)
