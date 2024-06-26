from typing import Any, ClassVar, Optional, Type

from pydantic_core.core_schema import (
    CoreSchema,
    ValidationInfo,
    int_schema,
    with_info_before_validator_function,
)

from eth_pydantic_types.validators import validate_int_size


class BaseInt(int):
    size: ClassVar[int] = 256
    signed: ClassVar[bool] = True

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> CoreSchema:
        return with_info_before_validator_function(cls.__eth_pydantic_validate__, int_schema())

    @classmethod
    def __eth_pydantic_validate__(cls, value: Any, info: Optional[ValidationInfo] = None) -> int:
        return cls(cls.validate_size(int(value)))

    @classmethod
    def validate_size(cls, value: int) -> int:
        return validate_int_size(value, cls.size, cls.signed)


class Int(BaseInt):
    """
    Represents an integer.
    This type is meant to be overridden by the larger types with a new size.
    e.g. Int32, Int64.
    """


class UInt(BaseInt):
    """
    Represents an unsigned integer.
    This type is meant to be overridden by the larger types with a new size.
    e.g. UInt32, UInt64.
    """

    signed = False


def _make_cls(
    size: int, base_type: Type, signed: bool = True, prefix: str = "", dict_additions: dict = {}
):
    if issubclass(base_type, int):
        display = "Int" if signed else "UInt"

    return type(
        f"{prefix}{display}{size}",
        (Int if signed else UInt,),
        dict(size=size, signed=signed, **dict_additions),
    )


Int8 = _make_cls(8, int)
Int16 = _make_cls(16, int)
Int32 = _make_cls(32, int)
Int64 = _make_cls(64, int)
Int128 = _make_cls(128, int)
Int256 = _make_cls(256, int)
UInt8 = _make_cls(8, int, signed=False)
UInt16 = _make_cls(16, int, signed=False)
UInt32 = _make_cls(32, int, signed=False)
UInt64 = _make_cls(64, int, signed=False)
UInt128 = _make_cls(128, int, signed=False)
UInt256 = _make_cls(256, int, signed=False)
