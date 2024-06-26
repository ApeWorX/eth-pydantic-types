import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.numbers import (
    Int8,
    Int16,
    Int32,
    Int64,
    Int128,
    Int256,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    UInt128,
    UInt256,
)


class SignedModel(BaseModel):
    valueint8: Int8
    valueint16: Int16
    valueint32: Int32
    valueint64: Int64
    valueint128: Int128
    valueint256: Int256

    @classmethod
    def from_single(cls, value):
        return cls(
            valueint8=value,
            valueint16=value,
            valueint32=value,
            valueint64=value,
            valueint128=value,
            valueint256=value,
        )


class UnsignedModel(BaseModel):
    valueuint8: UInt8
    valueuint16: UInt16
    valueuint32: UInt32
    valueuint64: UInt64
    valueuint128: UInt128
    valueuint256: UInt256

    @classmethod
    def from_single(cls, value):
        return cls(
            valueuint8=value,
            valueuint16=value,
            valueuint32=value,
            valueuint64=value,
            valueuint128=value,
            valueuint256=value,
        )


def test_negative_unsigned_int():
    with pytest.raises(ValidationError):
        UnsignedModel.from_single(-1)
