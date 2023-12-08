from typing import Any, ClassVar, Optional, Tuple, Union, cast

from eth_typing import HexStr as EthTypingHexStr
from eth_utils import add_0x_prefix
from hexbytes import HexBytes as BaseHexBytes
from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    ValidationInfo,
    bytes_schema,
    no_info_before_validator_function,
    str_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types._error import HexValueError
from eth_pydantic_types.serializers import hex_serializer

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
    schema_pattern: ClassVar[str] = schema_pattern
    schema_examples: ClassVar[Tuple[str, ...]] = schema_examples

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
        return BaseHexBytes(value)


class BaseHexStr(str, BaseHex):
    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None):
        return no_info_before_validator_function(cls.__eth_pydantic_validate__, str_schema())

    @classmethod
    def __eth_pydantic_validate__(cls, value):
        return value  # Override.

    @classmethod
    def from_bytes(cls, data: bytes) -> "BaseHexStr":
        hex_str = data.hex()
        return cls(hex_str if hex_str.startswith("0x") else hex_str)

    @classmethod
    def validate_hex(cls, data: Union[bytes, str, int]):
        if isinstance(data, bytes):
            return cls.from_bytes(data)

        elif isinstance(data, str):
            return validate_hex_str(data)

        elif isinstance(data, int):
            return BaseHexBytes(data).hex()

        raise HexValueError(data)

    def __int__(self) -> int:
        return int(self, 16)

    def __bytes__(self) -> bytes:
        return bytes.fromhex(self[2:])


class HexStr(BaseHexStr):
    """A hex string value, typically from a hash."""

    @classmethod
    def __eth_pydantic_validate__(cls, value):
        return cls.validate_hex(value)

    @classmethod
    def from_bytes(cls, data: bytes) -> "HexStr":
        value_str = super().from_bytes(data)
        value = add_0x_prefix(cast(EthTypingHexStr, value_str))
        return HexStr(value)


def validate_hex_str(value: str) -> str:
    hex_value = (value[2:] if value.startswith("0x") else value).lower()
    if set(hex_value) - set("1234567890abcdef"):
        raise HexValueError(value)

    # Missing zero padding.
    if len(hex_value) % 2 != 0:
        hex_value = f"0{hex_value}"

    return f"0x{hex_value}"
