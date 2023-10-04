from typing import Any, Optional

from hexbytes import HexBytes as BaseHexBytes
from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    ValidationInfo,
    bytes_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types.serializers import hex_serializer


class HexBytes(BaseHexBytes):
    """
    Use when receiving ``hexbytes.HexBytes`` values. Includes
    a pydantic validator and serializer.
    """

    def __get_pydantic_core_schema__(self, *args, **kwargs) -> CoreSchema:
        schema = with_info_before_validator_function(self._validate_hexbytes, bytes_schema())
        schema["serialization"] = hex_serializer
        return schema

    @classmethod
    def fromhex(cls, hex_str: str) -> "HexBytes":
        value = hex_str[2:] if hex_str.startswith("0x") else hex_str
        return super().fromhex(value)

    @classmethod
    def _validate_hexbytes(cls, value: Any, info: Optional[ValidationInfo] = None) -> BaseHexBytes:
        return BaseHexBytes(value)
