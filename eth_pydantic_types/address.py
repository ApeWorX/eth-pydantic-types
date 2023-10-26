from typing import Any, ClassVar, Optional, Tuple, cast

from eth_typing import ChecksumAddress
from eth_utils import is_checksum_address, to_checksum_address
from pydantic_core.core_schema import ValidationInfo, str_schema
from typing_extensions import Annotated

from eth_pydantic_types.hash import HashStr20

ADDRESS_PATTERN = "^0x[a-fA-F0-9]{40}$"


def address_schema():
    return str_schema(min_length=42, max_length=42, pattern=ADDRESS_PATTERN)


class Address(HashStr20):
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

    @classmethod
    def __eth_pydantic_validate__(cls, value: Any, info: Optional[ValidationInfo] = None) -> str:
        value = super().__eth_pydantic_validate__(value)
        return cls.to_checksum_address(value)

    @classmethod
    def to_checksum_address(cls, value: str) -> ChecksumAddress:
        return (
            cast(ChecksumAddress, value)
            if is_checksum_address(value)
            else to_checksum_address(value)
        )


"""
A type that can be used in place of ``eth_typing.ChecksumAddress``.

**NOTE**: We are unable to subclass ``eth_typing.ChecksumAddress``
  in :class:`~eth_pydantic_types.address.Address` because it is
  a NewType; that is why we offer this annotated approach.
"""
AddressType = Annotated[ChecksumAddress, Address]
