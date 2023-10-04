from typing import Any, ClassVar, Optional

from pydantic_core.core_schema import (
    CoreSchema,
    ValidationInfo,
    bytes_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types.hexbytes import HexBytes
from eth_pydantic_types.validators import validate_bytes_size


class Hash(HexBytes):
    """
    Represents a bytes32 data-type for a hash value and provides
    validation and serialization methods.
    """

    size: ClassVar[int]

    def __get_pydantic_core_schema__(self, *args, **kwargs) -> CoreSchema:
        return with_info_before_validator_function(
            self._validate_hash, bytes_schema(max_length=self.size)
        )

    @classmethod
    def _validate_hash(cls, value: Any, info: Optional[ValidationInfo] = None) -> bytes:
        return cls(cls.validate_size(HexBytes(value)))

    @classmethod
    def validate_size(cls, value: bytes) -> bytes:
        return validate_bytes_size(value, cls.size)


class Hash8(Hash):
    """
    A hash that is 8-bytes.
    """

    size: ClassVar[int] = 8


class Hash16(Hash):
    """
    A hash that is 16-bytes.
    """

    size: ClassVar[int] = 16


class Hash32(Hash):
    """
    A hash that is 32-bytes.
    """

    size: ClassVar[int] = 32


class Hash64(Hash):
    """
    A hash that is 64-bytes.
    """

    size: ClassVar[int] = 64
