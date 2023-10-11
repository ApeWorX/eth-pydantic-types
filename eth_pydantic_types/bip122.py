from typing import Any, Optional

from pydantic_core import CoreSchema, PydanticCustomError
from pydantic_core.core_schema import (
    str_schema,
    with_info_before_validator_function,
    ValidationInfo,
)

from eth_pydantic_types.hex import validate_hex_str
from eth_pydantic_types._error import Bip122UriFormatError


class Bip122Uri(str):
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

        validated_genesis_hash = validate_hex_str(genesis_hash)
        validated_block_hash = validate_hex_str(block_hash)
        return f"{prefix}{validated_genesis_hash}/{block_keyword}/{validated_block_hash}"
