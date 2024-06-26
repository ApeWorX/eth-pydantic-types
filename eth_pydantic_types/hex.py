from typing import Any, ClassVar, Optional, Tuple, Type, Union, cast

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
from eth_pydantic_types.validators import validate_bytes_size, validate_str_size

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
    bound: bool = False
    size: ClassVar[int] = 0
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
        schema = with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            bytes_schema(max_length=cls.size, min_length=cls.size) if cls.bound else bytes_schema(),
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
        return validate_bytes_size(value, cls.size) if cls.bound else value


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
    def __get_pydantic_core_schema__(cls, value, handler=None) -> CoreSchema:
        str_size = cls.size * 2 + 2
        return with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            str_schema(max_length=str_size, min_length=str_size) if cls.bound else str_schema(),
        )

    @classmethod
    def __eth_pydantic_validate__(cls, value: Any, info: Optional[ValidationInfo] = None) -> str:
        hex_str = cls.validate_hex(value)
        hex_value = hex_str[2:] if hex_str.startswith("0x") else hex_str
        sized_value = cls.validate_size(hex_value) if cls.bound else hex_value
        return cls(f"0x{sized_value}")

    @classmethod
    def validate_size(cls, value: str) -> str:
        return validate_str_size(value, cls.size * 2)

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


def get_hash_pattern(str_size: int) -> str:
    return f"^0x[a-fA-F0-9]{{{str_size}}}$"


def get_hash_examples(str_size: int) -> Tuple[str, str, str, str]:
    zero_hash = f"0x{'0' * str_size}"
    leading_zero = f"0x01{'1e' * ((str_size - 1) // 2)}"
    trailing_zero = f"0x{'1e' * ((str_size - 1) // 2)}10"
    full_hash = f"0x{'1e' * (str_size // 2)}"
    return zero_hash, leading_zero, trailing_zero, full_hash


def _make_cls(size: int, base_type: Type, prefix: str = "", dict_additions: dict = {}):
    str_size = size * 2
    display = "Bytes" if issubclass(base_type, bytes) else "Str"
    base_type = HexBytes if issubclass(base_type, bytes) else HexStr
    type_dict = dict(
        bound=True,
        size=size,
        schema_pattern=get_hash_pattern(str_size),
        schema_examples=get_hash_examples(str_size),
        **dict_additions,
    )
    return type(
        f"{prefix}{display}{size}",
        (base_type,),
        type_dict,
    )


# Creates bound variations e.g. HexStr16, HexStr64
HexBytes1 = _make_cls(1, bytes, prefix="Hex")
HexBytes4 = _make_cls(4, bytes, prefix="Hex")
HexBytes8 = _make_cls(8, bytes, prefix="Hex")
HexBytes16 = _make_cls(16, bytes, prefix="Hex")
HexBytes20 = _make_cls(20, bytes, prefix="Hex")
HexBytes32 = _make_cls(32, bytes, prefix="Hex")
HexBytes64 = _make_cls(64, bytes, prefix="Hex")
HexStr4 = _make_cls(4, str, prefix="Hex")
HexStr8 = _make_cls(8, str, prefix="Hex")
HexStr16 = _make_cls(16, str, prefix="Hex")
HexStr20 = _make_cls(20, str, prefix="Hex")
HexStr32 = _make_cls(32, str, prefix="Hex")
HexStr64 = _make_cls(64, str, prefix="Hex")
