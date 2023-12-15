from typing import Any, Callable, Dict, Optional, Sized, TypeVar, cast

from pydantic import WithJsonSchema
from pydantic_core.core_schema import bytes_schema

from eth_pydantic_types._error import SizeError

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

    raise SizeError(size, value)


def validate_bytes_size(value: bytes, size: int) -> bytes:
    return validate_size(value, size, coerce=lambda v: _coerce_hexbytes_size(v, size))


def validate_address_size(value: str) -> str:
    return validate_str_size(value, 40)


def validate_str_size(value: str, size: int) -> str:
    return validate_size(value, size, coerce=lambda v: _coerce_hexstr_size(v, size))


def _coerce_hexstr_size(val: str, length: int) -> str:
    val = val.replace("0x", "") if val.startswith("0x") else val
    if len(val) == length:
        return val

    val_stripped = val.lstrip("0")
    num_zeroes = max(0, length - len(val_stripped))
    zeroes = "0" * num_zeroes
    return f"{zeroes}{val_stripped}"


def _coerce_hexbytes_size(val: bytes, num_bytes: int) -> bytes:
    if len(val) == num_bytes:
        return val

    val_stripped = val.lstrip(b"\x00")
    num_zeroes = max(0, num_bytes - len(val_stripped))
    zeroes = b"\x00" * num_zeroes
    return zeroes + val_stripped
