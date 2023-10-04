from typing import Any, ClassVar, Optional

from pydantic_core.core_schema import (
    CoreSchema,
    ValidationInfo,
    bytes_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types.hexbytes import HexBytes
from eth_pydantic_types.serializers import hex_serializer
from eth_pydantic_types.validators import validate_bytes_size


class Hash(HexBytes):
    """
    Represents a single-slot static hash.
    The class variable "size" is overridden in subclasses for each byte-size,
    e.g. Hash4, Hash20, Hash32.
    """

    size: ClassVar[int] = 1

    def __get_pydantic_core_schema__(self, *args, **kwargs) -> CoreSchema:
        schema = with_info_before_validator_function(
            self._validate_hash, bytes_schema(max_length=self.size, min_length=self.size)
        )
        schema["serialization"] = hex_serializer
        return schema

    @classmethod
    def _validate_hash(cls, value: Any, info: Optional[ValidationInfo] = None) -> bytes:
        return cls(cls.validate_size(HexBytes(value)))

    @classmethod
    def validate_size(cls, value: bytes) -> bytes:
        return validate_bytes_size(value, cls.size)


class Hash4(Hash):
    """
    A hash that is 4-bytes.
    """

    size: ClassVar[int] = 4


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


class Hash20(Hash):
    """
    A hash that is 20-bytes.
    """

    size: ClassVar[int] = 20


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
