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

    @classmethod
    def from_series(cls, value8, value16, value32, value64, value128, value256):
        return cls(
            valueint8=value8,
            valueint16=value16,
            valueint32=value32,
            valueint64=value64,
            valueint128=value128,
            valueint256=value256,
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

    @classmethod
    def from_series(cls, value8, value16, value32, value64, value128, value256):
        return cls(
            valueuint8=value8,
            valueuint16=value16,
            valueuint32=value32,
            valueuint64=value64,
            valueuint128=value128,
            valueuint256=value256,
        )


def test_negative_unsigned_int():
    with pytest.raises(ValidationError):
        UnsignedModel.from_single(-1)


def test_retains_value():
    signed = SignedModel.from_series(-1, -2, -3, -4, -5, -6)
    assert signed.valueint8 == -1
    assert signed.valueint16 == -2
    assert signed.valueint32 == -3
    assert signed.valueint64 == -4
    assert signed.valueint128 == -5
    assert signed.valueint256 == -6

    unsigned = UnsignedModel.from_series(1, 2, 3, 4, 5, 6)
    assert unsigned.valueuint8 == 1
    assert unsigned.valueuint16 == 2
    assert unsigned.valueuint32 == 3
    assert unsigned.valueuint64 == 4
    assert unsigned.valueuint128 == 5
    assert unsigned.valueuint256 == 6


def test_upper_bounds():
    # Meets the upper bounds
    SignedModel.from_series(
        127,
        32767,
        2147483647,
        9223372036854775807,
        170141183460469231731687303715884105727,
        57896044618658097711785492504343953926634992332820282019728792003956564819967,
    )
    UnsignedModel.from_series(
        255,
        65535,
        4294967295,
        18446744073709551615,
        340282366920938463463374607431768211455,
        115792089237316195423570985008687907853269984665640564039457584007,
    )

    # Exceeds the upper bounds
    with pytest.raises(ValidationError):
        SignedModel.from_series(
            128,
            32768,
            2147483648,
            9223372036854775808,
            170141183460469231731687303715884105728,
            57896044618658097711785492504343953926634992332820282019728792003956564819968,
        )
    with pytest.raises(ValidationError):
        UnsignedModel.from_series(
            256,
            65536,
            4294967296,
            18446744073709551616,
            340282366920938463463374607431768211456,
            115792089237316195423570985008687907853269984665640564039457584008,
        )


def test_lower_bounds():
    # Meets the lower bounds
    SignedModel.from_series(
        -128,
        -32768,
        -2147483648,
        -9223372036854775808,
        -170141183460469231731687303715884105727,
        -57896044618658097711785492504343953926634992332820282019728792003956564819968,
    )
    UnsignedModel.from_series(0, 0, 0, 0, 0, 0)

    # Exceeds the lower bounds
    with pytest.raises(ValidationError):
        SignedModel.from_series(
            -129,
            -32769,
            -2147483649,
            -9223372036854775809,
            -170141183460469231731687303715884105728,
            -57896044618658097711785492504343953926634992332820282019728792003956564819969,
        )
    with pytest.raises(ValidationError):
        UnsignedModel.from_series(-1, -1, -1, -1, -1, -1)
