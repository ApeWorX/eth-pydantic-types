from typing import TYPE_CHECKING, Any, ClassVar, Optional

from hexbytes.main import HexBytes as BaseHexBytes
from pydantic_core.core_schema import (
    ValidationInfo,
    bytes_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types.hex.base import BaseHex
from eth_pydantic_types.serializers import hex_serializer
from eth_pydantic_types.utils import get_hash_examples, get_hash_pattern, validate_bytes_size

if TYPE_CHECKING:
    from pydantic_core import CoreSchema
    from typing_extensions import TypeAlias


class HexBytes(BaseHexBytes, BaseHex):
    """
    Use when receiving ``hexbytes.HexBytes`` values. Includes
    a pydantic validator and serializer.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handle=None) -> "CoreSchema":
        schema = with_info_before_validator_function(cls.__eth_pydantic_validate__, bytes_schema())
        schema["serialization"] = hex_serializer
        return schema

    @classmethod
    def fromhex(cls, hex_str: str) -> "HexBytes":
        value = hex_str[2:] if hex_str.startswith("0x") else hex_str
        return super().fromhex(value)

    @classmethod
    def __eth_pydantic_validate__(
        cls, value: Any, info: Optional[ValidationInfo] = None
    ) -> BaseHexBytes:
        return cls(cls.validate_size(HexBytes(value)))

    @classmethod
    def validate_size(cls, value: bytes) -> bytes:
        return value


class BoundHexBytes(HexBytes):
    """
    Use when receiving ``hexbytes.HexBytes`` values and a specific size is required.
    Includes a pydantic validator and serializer.
    """

    size: ClassVar[int] = 32

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handle=None) -> "CoreSchema":
        schema = with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            bytes_schema(max_length=cls.size, min_length=cls.size),
        )
        schema["serialization"] = hex_serializer
        return schema

    @classmethod
    def validate_size(cls, value: bytes) -> bytes:
        str_size = cls.size * 2
        cls.schema_pattern = get_hash_pattern(str_size)
        cls.schema_examples = get_hash_examples(str_size)
        return validate_bytes_size(value, cls.size)


class HexBytes20(BoundHexBytes):
    size: ClassVar[int] = 20


HexBytes32: "TypeAlias" = BoundHexBytes
