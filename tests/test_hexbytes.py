import pytest
from hexbytes import HexBytes as BaseHexBytes
from pydantic import BaseModel

from eth_pydantic_types.hexbytes import HexBytes


class Model(BaseModel):
    value: HexBytes
    """The user declares their value to be our annotated type."""


@pytest.mark.parametrize("value", ("0xa", 10, b"\n"))
def test_model(value):
    actual = Model(value=value)

    # The end result, the value is a hexbytes.HexBytes
    assert actual.value == BaseHexBytes(value)
    assert actual.value.hex() == "0x0a"
    assert isinstance(actual.value, bytes)
    assert isinstance(actual.value, BaseHexBytes)


def test_fromhex(bytes32str):
    actual_with_0x = HexBytes.fromhex(bytes32str)
    actual_without_0x = HexBytes.fromhex(bytes32str[2:])
    expected = HexBytes(bytes32str)
    assert actual_with_0x == actual_without_0x == expected
