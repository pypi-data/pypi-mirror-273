from typing import (Callable, Optional, TypeVar, Union, dataclass_transform,
                    overload)

from devtools.attrs.field import Field, FieldInfo, info
from devtools.attrs.main import define

T = TypeVar("T")

ReturnT = Union[Callable[[type[T]], type[T]], type[T]]
OptionalTypeT = Optional[type[T]]


@overload
def mutable(
    maybe_cls: None = None,
    /,
    *,
    init: bool = True,
    kw_only: bool = False,
    slots: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = True,
    hash: Optional[bool] = False,
    pydantic: bool = False,
    dataclasses_field: bool = False,
    field_class: type[Field] = Field,
    alias_generator: Callable[[str], str] = str,
) -> Callable[[type[T]], type[T]]:
    ...


@overload
def mutable(
    maybe_cls: type[T],
    /,
    *,
    init: bool = True,
    kw_only: bool = False,
    slots: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = True,
    hash: Optional[bool] = None,
    pydantic: bool = False,
    dataclass_fields: bool = False,
    field_class: type[Field] = Field,
    alias_generator: Callable[[str], str] = str,
) -> type[T]:
    ...


@dataclass_transform(
    order_default=True,
    frozen_default=False,
    kw_only_default=False,
    field_specifiers=(FieldInfo, info),
)
def mutable(
    maybe_cls: OptionalTypeT[T] = None,
    /,
    *,
    init: bool = True,
    kw_only: bool = False,
    slots: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = True,
    hash: Optional[bool] = None,
    pydantic: bool = False,
    dataclass_fields: bool = False,
    field_class: type[Field] = Field,
    alias_generator: Callable[[str], str] = str,
) -> ReturnT[T]:
    return define(
        maybe_cls,
        frozen=False,
        init=init,
        kw_only=kw_only,
        slots=slots,
        repr=repr,
        eq=eq,
        order=order,
        hash=hash,
        pydantic=pydantic,
        dataclass_fields=dataclass_fields,
        field_class=field_class,
        alias_generator=alias_generator,
    )


@overload
def kw_only(
    maybe_cls: None = None,
    /,
    *,
    frozen: bool = False,
    init: bool = True,
    slots: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = True,
    hash: Optional[bool] = None,
    pydantic: bool = False,
    dataclass_fields: bool = False,
    field_class: type[Field] = Field,
    alias_generator: Callable[[str], str] = str,
) -> Callable[[type[T]], type[T]]:
    ...


@overload
def kw_only(
    maybe_cls: type[T],
    /,
    *,
    frozen: bool = False,
    init: bool = True,
    slots: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = True,
    hash: Optional[bool] = None,
    pydantic: bool = False,
    dataclass_fields: bool = False,
    field_class: type[Field] = Field,
    alias_generator: Callable[[str], str] = str,
) -> type[T]:
    ...


@dataclass_transform(
    order_default=True,
    frozen_default=True,
    kw_only_default=True,
    field_specifiers=(FieldInfo, info),
)
def kw_only(
    maybe_cls: OptionalTypeT[T] = None,
    /,
    *,
    frozen: bool = True,
    init: bool = True,
    slots: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = True,
    hash: Optional[bool] = None,
    pydantic: bool = False,
    dataclass_fields: bool = False,
    field_class: type[Field] = Field,
    alias_generator: Callable[[str], str] = str,
) -> ReturnT[T]:
    return define(
        maybe_cls,
        frozen=frozen,
        init=init,
        kw_only=True,
        slots=slots,
        repr=repr,
        eq=eq,
        order=order,
        hash=hash,
        pydantic=pydantic,
        dataclass_fields=dataclass_fields,
        field_class=field_class,
        alias_generator=alias_generator,
    )


@overload
def schema_class(
    maybe_cls: None = None,
    /,
    *,
    frozen: bool = False,
    init: bool = True,
    slots: bool = False,
    repr: bool = True,
    eq: bool = True,
    order: bool = True,
    hash: Optional[bool] = None,
    pydantic: bool = False,
    dataclass_fields: bool = False,
    field_class: type[Field] = Field,
    alias_generator: Callable[[str], str] = str,
) -> Callable[[type[T]], type[T]]:
    ...


@overload
def schema_class(
    maybe_cls: type[T],
    /,
    *,
    frozen: bool = False,
    init: bool = False,
    kw_only: bool = False,
    slots: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = True,
    hash: Optional[bool] = None,
    dataclass_fields: bool = False,
    field_class: type[Field] = Field,
    alias_generator: Callable[[str], str] = str,
) -> type[T]:
    ...


@dataclass_transform(
    order_default=True,
    frozen_default=True,
    kw_only_default=False,
    field_specifiers=(FieldInfo, info),
)
def schema_class(
    maybe_cls: OptionalTypeT[T] = None,
    /,
    *,
    frozen: bool = True,
    init: bool = True,
    kw_only: bool = False,
    slots: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = True,
    hash: Optional[bool] = None,
    dataclass_fields: bool = False,
    field_class: type[Field] = Field,
    alias_generator: Callable[[str], str] = str,
) -> ReturnT[T]:
    return define(
        maybe_cls,
        frozen=frozen,
        init=init,
        kw_only=kw_only,
        slots=slots,
        repr=repr,
        eq=eq,
        order=order,
        hash=hash,
        pydantic=True,
        dataclass_fields=dataclass_fields,
        field_class=field_class,
        alias_generator=alias_generator,
    )
