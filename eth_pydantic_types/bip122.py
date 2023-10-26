from enum import Enum
from functools import cached_property
from typing import Any, Optional, Tuple

from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    ValidationInfo,
    str_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types._error import Bip122UriFormatError
from eth_pydantic_types.hex import validate_hex_str


class Bip122UriType(Enum):
    TX = "tx"
    BLOCK = "block"
    ADDRESS = "address"


class Bip122Uri(str):
    prefix: str = "blockchain://"

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        example = (
            f"{cls.prefix}d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3"
            f"/{Bip122UriType.BLOCK.value}/"
            f"752820c0ad7abc1200f9ad42c4adc6fbb4bd44b5bed4667990e64565102c1ba6"
        )
        pattern = f"^{cls.prefix}[0-9a-f]{{64}}/{Bip122UriType.BLOCK.value}/[0-9a-f]{{64}}$"
        json_schema.update(examples=[example], pattern=pattern)
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> CoreSchema:
        return with_info_before_validator_function(
            value.__eth_pydantic_validate__,
            str_schema(),
        )

    @classmethod
    def __eth_pydantic_validate__(cls, value: Any, info: Optional[ValidationInfo] = None) -> str:
        if not value.startswith(cls.prefix):
            raise Bip122UriFormatError(value)

        genesis_hash, block_keyword, block_hash = cls.parse(value)
        return f"{cls.prefix}{genesis_hash[2:]}/{block_keyword.value}/{block_hash[2:]}"

    @classmethod
    def parse(cls, value: str) -> Tuple[str, Bip122UriType, str]:
        protocol_suffix = value.replace(cls.prefix, "")
        protocol_parsed = protocol_suffix.split("/")
        if len(protocol_parsed) != 3:
            raise Bip122UriFormatError(value)

        genesis_hash, block_keyword, block_hash = protocol_parsed
        block_keyword = block_keyword.lower()
        if block_keyword not in [x.value for x in Bip122UriType]:
            raise Bip122UriFormatError(value)

        return (
            validate_hex_str(genesis_hash),
            Bip122UriType(block_keyword),
            validate_hex_str(block_hash),
        )

    @cached_property
    def parsed(self) -> Tuple[str, Bip122UriType, str]:
        return self.parse(self)

    @property
    def chain(self) -> str:
        return self.parsed[0]

    @property
    def uri_type(self) -> Bip122UriType:
        return self.parsed[1]

    @property
    def hash(self) -> str:
        return self.parsed[2]
