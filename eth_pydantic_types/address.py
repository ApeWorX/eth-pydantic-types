from typing import Any, Optional

from eth_utils import is_checksum_address, to_checksum_address
from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    ValidationInfo,
    str_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types.hexbytes import HexBytes
from eth_pydantic_types.validators import validate_address_size


class Address(str):
    """
    Use for address-types. Validates as a checksummed address. Left-pads zeroes
    if necessary.
    """

    def __get_pydantic_core_schema__(self, *args, **kwargs) -> CoreSchema:
        schema = with_info_before_validator_function(
            self._validate_address,
            str_schema(min_length=42, max_length=42, pattern="^0x[a-fA-F0-9]{40}$"),
        )
        return schema

    @classmethod
    def _validate_address(cls, value: Any, info: Optional[ValidationInfo] = None) -> str:
        if isinstance(value, str) and is_checksum_address(value):
            return value

        elif not isinstance(value, str):
            value = HexBytes(value).hex()

        number = value[2:] if value.startswith("0x") else value
        number_padded = validate_address_size(number, 40)
        value = f"0x{number_padded}"
        return to_checksum_address(value)

    def __int__(self) -> int:
        return int(self, 16)

    def __bytes__(self) -> HexBytes:
        return HexBytes(self)
