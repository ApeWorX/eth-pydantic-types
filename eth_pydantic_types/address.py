from functools import cached_property
from typing import TYPE_CHECKING, Annotated, Any, ClassVar, Optional

from cchecksum import to_checksum_address
from eth_typing import ChecksumAddress
from pydantic_core.core_schema import (
    ValidationInfo,
    str_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types.hex import HexStr20

if TYPE_CHECKING:
    from pydantic_core import CoreSchema

ADDRESS_PATTERN = "^0x[a-fA-F0-9]{40}$"


def address_schema():
    return str_schema(min_length=42, max_length=42, pattern=ADDRESS_PATTERN)


class Address(HexStr20):
    """
    Use for address-types. Validates as a checksummed address. Left-pads zeroes
    if necessary.
    """

    schema_pattern: ClassVar[str] = ADDRESS_PATTERN
    schema_examples: ClassVar[tuple[str, ...]] = (
        "0x0000000000000000000000000000000000000000",  # Zero address
        "0x02c84e944F97F4A4f60221e6fb5d5DbAE49c7aaB",  # Leading zero
        "0xa5a13f62ce1113838e0d9b4559b8caf5f76463c0",  # Trailing zero
        "0x1e59ce931B4CFea3fe4B875411e280e173cB7A9C",
    )

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> "CoreSchema":
        return with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            address_schema(),
        )

    @classmethod
    def __eth_pydantic_validate__(cls, value: Any, info: Optional[ValidationInfo] = None) -> str:
        value = super().__eth_pydantic_validate__(value)
        return cls.to_checksum_address(value)

    @classmethod
    def update_schema(cls):
        # Already set statically in the class
        return

    @classmethod
    def to_checksum_address(cls, value: str) -> ChecksumAddress:
        return to_checksum_address(value)


class _AddressTypeFactory:
    @cached_property
    def address_type(self):
        # Lazy define for performance reasons.
        AddressType = Annotated[ChecksumAddress, Address]
        AddressType.__doc__ = """
        A type that can be used in place of ``eth_typing.ChecksumAddress``.

        **NOTE**: We are unable to subclass ``eth_typing.ChecksumAddress``
          in :class:`~eth_pydantic_types.address.Address` because it is
          a NewType; that is why we offer this annotated approach.
        """
        return AddressType


_factory = _AddressTypeFactory()


def __getattr__(name: str):
    if name == "Address":
        return Address

    elif name == "AddressType":
        return _factory.address_type


__all__ = [
    "Address",
    "Address",
]
