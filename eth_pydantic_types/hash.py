from typing import Any, ClassVar, Optional, Tuple

from pydantic_core.core_schema import (
    CoreSchema,
    ValidationInfo,
    bytes_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types.hex import HexBytes
from eth_pydantic_types.serializers import hex_serializer
from eth_pydantic_types.validators import validate_bytes_size


def get_hash_pattern(size: int) -> str:
    return f"^0x[a-fA-F0-9]{{{size}}}$"


def get_hash_examples(size: int) -> Tuple[str, str]:
    return f"0x{'0' * (size * 2)}", f"0x{'1e' * size}"


class Hash(HexBytes):
    """
    Represents a single-slot static hash.
    The class variable "size" is overridden in subclasses for each byte-size,
    e.g. Hash4, Hash20, Hash32.
    """

    size: ClassVar[int] = 1
    schema_pattern: ClassVar[str] = get_hash_pattern(1)
    schema_examples: ClassVar[Tuple[str, ...]] = get_hash_examples(1)

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


def make_hash_cls(size: int):
    return type(
        f"Hash{size}",
        (Hash,),
        dict(
            size=size,
            schema_pattern=get_hash_pattern(size),
            schema_examples=get_hash_examples(size),
        ),
    )


Hash4 = make_hash_cls(4)
Hash8 = make_hash_cls(8)
Hash16 = make_hash_cls(16)
Hash20 = make_hash_cls(20)
Hash32 = make_hash_cls(32)
Hash64 = make_hash_cls(64)
