from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Optional,
    Union,
)

from pydantic_core.core_schema import (
    ValidationInfo,
    int_schema,
    no_info_before_validator_function,
    with_info_before_validator_function,
)

from eth_pydantic_types._error import HexValueError
from eth_pydantic_types.hex.base import BaseHex
from eth_pydantic_types.serializers import create_hex_serializer, hex_serializer
from eth_pydantic_types.utils import (
    PadDirection,
    get_hash_examples,
    get_hash_pattern,
    validate_hex_str,
    validate_int_size,
)

if TYPE_CHECKING:
    from pydantic_core import CoreSchema
    from typing_extensions import TypeAlias


class BaseHexInt(int, BaseHex):
    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None):
        return no_info_before_validator_function(cls.__eth_pydantic_validate__, int_schema())

    @classmethod
    def __eth_pydantic_validate__(cls, value, **kwargs):
        return value  # Override.

    @classmethod
    def from_bytes(cls, data, byteorder: str = "big", signed: bool = False) -> "BaseHexInt":
        int_value = int.from_bytes(data, byteorder="big", signed=signed)
        return cls(int_value)

    @classmethod
    def validate_hex(cls, data: Union[bytes, str, int]):
        if isinstance(data, int):
            return cls(data)

        elif isinstance(data, bytes):
            return cls.from_bytes(data)

        elif isinstance(data, str):
            return cls(int(validate_hex_str(data), 16))

        raise HexValueError(data)

    def __bytes__(self) -> bytes:
        return self.to_bytes(self.size, byteorder="big")


class HexInt(BaseHexInt):
    """A hex int value."""

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> "CoreSchema":
        schema = with_info_before_validator_function(cls.__eth_pydantic_validate__, int_schema())
        schema["serialization"] = hex_serializer
        return schema

    @classmethod
    def __eth_pydantic_validate__(
        cls, value: Any, info: Optional[ValidationInfo] = None, **kwargs
    ) -> int:
        return cls(cls.validate_hex(value))


class BoundHexInt(BaseHexInt):
    """A hex string value, that is required to be a specific size."""

    size: ClassVar[int] = 32
    signed: ClassVar[bool] = False

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> "CoreSchema":
        if cls.signed:
            min_int = -(2 ** (8 * cls.size - 1))
            max_int = 2 ** (8 * cls.size - 1) - 1
        else:
            min_int = 0
            max_int = 2 ** (8 * cls.size) - 1

        schema = with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            int_schema(le=max_int, ge=min_int),
        )

        # NOTE: Integers should always pad left; else the value increases.
        schema["serialization"] = create_hex_serializer(size=cls.size, pad=PadDirection.LEFT)

        return schema

    @classmethod
    def __eth_pydantic_validate__(
        cls, value: Any, info: Optional[ValidationInfo] = None, **kwargs
    ) -> int:
        hex_int = cls.validate_hex(value)
        sized_value = cls.validate_size(hex_int)
        return cls(sized_value)

    @classmethod
    def validate_size(cls, value: int) -> int:
        cls.update_schema()
        return validate_int_size(value, cls.size, cls.signed)

    @classmethod
    def update_schema(cls):
        str_size = cls.size * 2
        cls.schema_pattern = get_hash_pattern(str_size)
        cls.schema_examples = get_hash_examples(str_size)


class HexInt32(BoundHexInt):
    size: ClassVar[int] = 32


# UInt256 is a common name for this type across other EVM packages, hence this alias.
UInt256: "TypeAlias" = HexInt32
