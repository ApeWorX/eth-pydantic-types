from typing import TYPE_CHECKING, Any, ClassVar

from hexbytes.main import HexBytes as BaseHexBytes
from pydantic_core.core_schema import (
    ValidationInfo,
    no_info_before_validator_function,
    str_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types._error import HexValueError
from eth_pydantic_types.hex.base import BaseHex
from eth_pydantic_types.utils import (
    PadDirection,
    get_hash_examples,
    get_hash_pattern,
    validate_hex_str,
    validate_str_size,
)

if TYPE_CHECKING:
    from pydantic_core import CoreSchema
    from typing_extensions import TypeAlias


class BaseHexStr(str, BaseHex):
    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None):
        return no_info_before_validator_function(cls.__eth_pydantic_validate__, str_schema())

    @classmethod
    def __eth_pydantic_validate__(cls, value, **kwargs):
        return value  # Override.

    @classmethod
    def from_bytes(cls, data: bytes) -> "BaseHexStr":
        hex_value = data.hex()
        hex_str = hex_value if hex_value.startswith("0x") else f"0x{hex_value}"
        return cls(hex_str)

    @classmethod
    def validate_hex(cls, data: bytes | str | int, prefixed: bool = True):
        if isinstance(data, bytes):
            result = cls.from_bytes(data)
        elif isinstance(data, str):
            result = validate_hex_str(data)
        elif isinstance(data, int):
            hex_value = BaseHexBytes(data).hex()
            result = hex_value if hex_value.startswith("0x") else f"0x{hex_value}"
        else:
            raise HexValueError(data)

        if not prefixed and result.startswith("0x"):
            return result[2:]

        return result

    def __int__(self) -> int:
        return int(self, 16)

    def __bytes__(self) -> bytes:
        return bytes.fromhex(self[2:])


class HexStr(BaseHexStr):
    """A hex string value."""

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> "CoreSchema":
        return with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            str_schema(),
        )

    @classmethod
    def __eth_pydantic_validate__(
        cls, value: Any, info: ValidationInfo | None = None, **kwargs
    ) -> str:
        hex_str = cls.validate_hex(value)
        hex_value = hex_str[2:] if hex_str.startswith("0x") else hex_str
        return cls(f"0x{hex_value}")

    @classmethod
    def from_bytes(cls, data: bytes) -> "HexStr":
        value_str = super().from_bytes(data)
        value = value_str if value_str.startswith("0x") else f"0x{value_str}"
        return HexStr(value)


class BoundHexStr(BaseHexStr):
    """A hex string value, that is required to be a specific size."""

    size: ClassVar[int] = 32

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> "CoreSchema":
        str_size = cls.size * 2 + 2
        return with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            str_schema(max_length=str_size, min_length=str_size),
        )

    @classmethod
    def __eth_pydantic_validate__(
        cls, value: Any, info: ValidationInfo | None = None, **kwargs
    ) -> str:
        if not (pad := kwargs.pop("pad", None)):
            # Integers are always padded to the left, but bytes-types are padded to the right
            # to be ABI-encode compliant.
            pad = PadDirection.LEFT if isinstance(value, int) else PadDirection.RIGHT

        prefixed = kwargs.pop("prefixed", True)
        hex_str = cls.validate_hex(value, prefixed=False)
        sized_value = cls.validate_size(hex_str, pad_direction=pad)
        return cls(f"0x{sized_value}") if prefixed else cls(sized_value)

    @classmethod
    def validate_size(cls, value: str, pad_direction: PadDirection = PadDirection.LEFT) -> str:
        cls.update_schema()
        return validate_str_size(value, cls.size * 2, pad_direction=pad_direction)

    @classmethod
    def update_schema(cls):
        str_size = cls.size * 2
        cls.schema_pattern = get_hash_pattern(str_size)
        cls.schema_examples = get_hash_examples(str_size)


class HexStr20(BoundHexStr):
    size: ClassVar[int] = 20


HexStr32: "TypeAlias" = BoundHexStr
