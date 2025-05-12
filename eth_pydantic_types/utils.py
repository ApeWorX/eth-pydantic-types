from collections.abc import Sized
from typing import TYPE_CHECKING, Callable, Optional, TypeVar

from eth_pydantic_types._error import HexValueError, SizeError

if TYPE_CHECKING:
    __SIZED_T = TypeVar("__SIZED_T", bound=Sized)


def validate_size(value: "__SIZED_T", size: int, coerce: Optional[Callable] = None) -> "__SIZED_T":
    if len(value) == size:
        return value

    elif coerce:
        return validate_size(coerce(value), size)

    raise SizeError(size, value)


def validate_in_range(value: int, size: int, signed: bool = True) -> int:
    if signed:
        if -(2**size) / 2 <= value < (2**size) / 2:
            return value

    else:
        if 0 <= value < 2**size:
            return value

    raise SizeError(size, value)


def validate_bytes_size(value: bytes, size: int) -> bytes:
    return validate_size(value, size, coerce=lambda v: _coerce_hexbytes_size(v, size))


def validate_address_size(value: str) -> str:
    return validate_str_size(value, 40)


def validate_str_size(value: str, size: int) -> str:
    return validate_size(value, size, coerce=lambda v: _coerce_hexstr_size(v, size))


def validate_int_size(value: int, size: int, signed: bool) -> int:
    return validate_in_range(value, size, signed)


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


def validate_hex_str(value: str) -> str:
    hex_value = (value[2:] if value.startswith("0x") else value).lower()
    if set(hex_value) - set("1234567890abcdef"):
        raise HexValueError(value)

    # Missing zero padding.
    if len(hex_value) % 2 != 0:
        hex_value = f"0{hex_value}"

    return f"0x{hex_value}"


def get_hash_pattern(str_size: int) -> str:
    return f"^0x[a-fA-F0-9]{{{str_size}}}$"


def get_hash_examples(str_size: int) -> tuple[str, str, str, str]:
    zero_hash = f"0x{'0' * str_size}"
    leading_zero = f"0x01{'1e' * ((str_size - 1) // 2)}"
    trailing_zero = f"0x{'1e' * ((str_size - 1) // 2)}10"
    full_hash = f"0x{'1e' * (str_size // 2)}"
    return zero_hash, leading_zero, trailing_zero, full_hash
