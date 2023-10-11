from typing import Any, Optional

from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    ValidationInfo,
    str_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types._error import Bip122UriFormatError
from eth_pydantic_types.hex import validate_hex_str


class Bip122Uri(str):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        example = (
            "blockchain://d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3"
            "/block/752820c0ad7abc1200f9ad42c4adc6fbb4bd44b5bed4667990e64565102c1ba6"
        )
        pattern = "^blockchain://[0-9a-f]{64}/block/[0-9a-f]{64}$"
        json_schema.update(examples=[example], pattern=pattern)
        return json_schema

    def __get_pydantic_core_schema__(self, *args, **kwargs) -> CoreSchema:
        schema = with_info_before_validator_function(
            self._validate,
            str_schema(),
        )
        return schema

    @classmethod
    def _validate(cls, value: Any, info: Optional[ValidationInfo] = None) -> str:
        prefix = "blockchain://"
        if not value.startswith(prefix):
            raise Bip122UriFormatError(value)

        protocol_suffix = value.replace(prefix, "")
        protocol_parsed = protocol_suffix.split("/")
        if len(protocol_parsed) != 3:
            raise Bip122UriFormatError(value)

        genesis_hash, block_keyword, block_hash = protocol_parsed

        if block_keyword != "block":
            raise Bip122UriFormatError(value)

        validated_genesis_hash = validate_hex_str(genesis_hash)[2:]
        validated_block_hash = validate_hex_str(block_hash)[2:]
        return f"{prefix}{validated_genesis_hash}/{block_keyword}/{validated_block_hash}"
