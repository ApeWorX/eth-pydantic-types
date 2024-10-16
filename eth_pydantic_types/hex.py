from typing import Any, ClassVar, Optional, Union, cast

from eth_typing import HexStr as EthTypingHexStr
from eth_utils import add_0x_prefix
from hexbytes.main import HexBytes as BaseHexBytes
from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    ValidationInfo,
    bytes_schema,
    no_info_before_validator_function,
    str_schema,
    with_info_before_validator_function,
)
from typing_extensions import TypeAlias

from eth_pydantic_types._error import HexValueError
from eth_pydantic_types.serializers import hex_serializer
from eth_pydantic_types.utils import (
    get_hash_examples,
    get_hash_pattern,
    validate_bytes_size,
    validate_hex_str,
    validate_str_size,
)

schema_pattern = "^0x([0-9a-f][0-9a-f])*$"
schema_examples = (
    "0x",  # empty bytes
    "0xd4",
    "0xd4e5",
    "0xd4e56740",
    "0xd4e56740f876aef8",
    "0xd4e56740f876aef8c010b86a40d5f567",
    "0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3",
)


class BaseHex:
    size: ClassVar[int] = 0
    schema_pattern: ClassVar[str] = schema_pattern
    schema_examples: ClassVar[tuple[str, ...]] = schema_examples

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(
            format="binary", pattern=cls.schema_pattern, examples=list(cls.schema_examples)
        )
        return json_schema


class HexBytes(BaseHexBytes, BaseHex):
    """
    Use when receiving ``hexbytes.HexBytes`` values. Includes
    a pydantic validator and serializer.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handle=None) -> CoreSchema:
        schema = with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            bytes_schema(),
        )
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
    def __get_pydantic_core_schema__(cls, value, handle=None) -> CoreSchema:
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


HexBytes32: TypeAlias = BoundHexBytes


class BaseHexStr(str, BaseHex):
    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None):
        return no_info_before_validator_function(cls.__eth_pydantic_validate__, str_schema())

    @classmethod
    def __eth_pydantic_validate__(cls, value):
        return value  # Override.

    @classmethod
    def from_bytes(cls, data: bytes) -> "BaseHexStr":
        hex_value = data.hex()
        hex_str = hex_value if hex_value.startswith("0x") else f"0x{hex_value}"
        return cls(hex_str)

    @classmethod
    def validate_hex(cls, data: Union[bytes, str, int]):
        if isinstance(data, bytes):
            return cls.from_bytes(data)

        elif isinstance(data, str):
            return validate_hex_str(data)

        elif isinstance(data, int):
            hex_value = BaseHexBytes(data).hex()
            return hex_value if hex_value.startswith("0x") else f"0x{hex_value}"

        raise HexValueError(data)

    def __int__(self) -> int:
        return int(self, 16)

    def __bytes__(self) -> bytes:
        return bytes.fromhex(self[2:])


class HexStr(BaseHexStr):
    """A hex string value, typically from a hash."""

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> CoreSchema:
        return with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            str_schema(),
        )

    @classmethod
    def __eth_pydantic_validate__(cls, value: Any, info: Optional[ValidationInfo] = None) -> str:
        hex_str = cls.validate_hex(value)
        hex_value = hex_str[2:] if hex_str.startswith("0x") else hex_str
        sized_value = hex_value
        return cls(f"0x{sized_value}")

    @classmethod
    def from_bytes(cls, data: bytes) -> "HexStr":
        value_str = super().from_bytes(data)
        value = add_0x_prefix(cast(EthTypingHexStr, value_str))
        return HexStr(value)


class BoundHexStr(BaseHexStr):
    """A hex string value, typically from a hash, that is required to be a specific size."""

    size: ClassVar[int] = 32
    calculate_schema: ClassVar[bool] = True

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> CoreSchema:
        str_size = cls.size * 2 + 2
        return with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            str_schema(max_length=str_size, min_length=str_size),
        )

    @classmethod
    def __eth_pydantic_validate__(cls, value: Any, info: Optional[ValidationInfo] = None) -> str:
        hex_str = cls.validate_hex(value)
        hex_value = hex_str[2:] if hex_str.startswith("0x") else hex_str
        sized_value = cls.validate_size(hex_value)
        return cls(f"0x{sized_value}")

    @classmethod
    def validate_size(cls, value: str) -> str:
        if cls.calculate_schema:
            str_size = cls.size * 2
            cls.schema_pattern = get_hash_pattern(str_size)
            cls.schema_examples = get_hash_examples(str_size)
        return validate_str_size(value, cls.size * 2)


class HexStr20(BoundHexStr):
    size: ClassVar[int] = 20


HexStr32: TypeAlias = BoundHexStr
