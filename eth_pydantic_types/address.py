from typing import Any, ClassVar, Optional, Tuple

from eth_utils import is_checksum_address, to_checksum_address
from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    ValidationInfo,
    str_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types.hex import BaseHexStr, HexBytes
from eth_pydantic_types.validators import validate_address_size

ADDRESS_PATTERN = "^0x[a-fA-F0-9]{40}$"


def address_schema():
    return str_schema(min_length=42, max_length=42, pattern=ADDRESS_PATTERN)


class Address(BaseHexStr):
    """
    Use for address-types. Validates as a checksummed address. Left-pads zeroes
    if necessary.
    """

    schema_pattern: ClassVar[str] = ADDRESS_PATTERN
    schema_examples: ClassVar[Tuple[str, ...]] = (
        "0x0000000000000000000000000000000000000000",  # Zero address
        "0x02c84e944F97F4A4f60221e6fb5d5DbAE49c7aaB",  # Leading zero
        "0xa5a13f62ce1113838e0d9b4559b8caf5f76463c0",  # Trailing zero
        "0x1e59ce931B4CFea3fe4B875411e280e173cB7A9C",
    )

    def __get_pydantic_core_schema__(self, *args, **kwargs) -> CoreSchema:
        schema = with_info_before_validator_function(
            self._validate_address,
            address_schema(),
        )
        return schema

    @classmethod
    def _validate_address(cls, value: Any, info: Optional[ValidationInfo] = None) -> str:
        if isinstance(value, str) and is_checksum_address(value):
            return value

        elif not isinstance(value, str):
            value = HexBytes(value).hex()

        number = value[2:] if value.startswith("0x") else value
        number_padded = validate_address_size(number)
        value = f"0x{number_padded}"
        return to_checksum_address(value)
