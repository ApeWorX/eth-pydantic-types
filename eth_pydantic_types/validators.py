from typing import Any, Callable, Dict, Optional, Sized, TypeVar, cast

from pydantic import WithJsonSchema
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import bytes_schema

__SIZED_T = TypeVar("__SIZED_T", bound=Sized)


class WithBytesSchema(WithJsonSchema):
    def __init__(self, **kwargs):
        mode = kwargs.pop("mode", None)
        schema = cast(Dict[str, Any], bytes_schema(**kwargs))
        super().__init__(schema, mode=mode)


def validate_size(value: __SIZED_T, size: int, coerce: Optional[Callable] = None) -> __SIZED_T:
    if len(value) == size:
        return value

    elif coerce:
        return validate_size(coerce(value), size)

    raise PydanticCustomError("value_size", "Invalid size of value", {"size": size, "value": value})


def validate_bytes_size(value: bytes, size: int) -> bytes:
    return validate_size(value, size, coerce=lambda v: _left_pad_bytes(v, size))


def validate_address_size(value: str, size: int) -> str:
    return validate_size(value, size, coerce=lambda v: _left_pad_str(v, size))


def _left_pad_str(val: str, num_bytes: int) -> str:
    return "0" * (num_bytes - len(val)) + val if len(val) < num_bytes else val


def _left_pad_bytes(val: bytes, num_bytes: int) -> bytes:
    return b"\x00" * (num_bytes - len(val)) + val if len(val) < num_bytes else val
