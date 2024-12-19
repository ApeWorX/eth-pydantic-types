import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.abi import (
    int8,
    int16,
    int32,
    int64,
    int128,
    int256,
    uint8,
    uint16,
    uint32,
    uint64,
    uint128,
    uint256,
)


class SignedModel(BaseModel):
    valueint8: int8
    valueint16: int16
    valueint32: int32
    valueint64: int64
    valueint128: int128
    valueint256: int256

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
    valueuint8: uint8
    valueuint16: uint16
    valueuint32: uint32
    valueuint64: uint64
    valueuint128: uint128
    valueuint256: uint256

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
