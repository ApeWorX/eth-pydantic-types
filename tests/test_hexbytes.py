import pytest
from hexbytes import HexBytes as BaseHexBytes
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hexbytes import HexBytes


class Model(BaseModel):
    value: HexBytes
    """The user declares their value to be our annotated type."""


@pytest.mark.parametrize("value", ("0xa", 10, b"\n"))
def test_hexbytes(value):
    actual = Model(value=value)

    # The end result, the value is a hexbytes.HexBytes
    assert actual.value == BaseHexBytes(value)
    assert actual.value.hex() == "0x0a"
    assert isinstance(actual.value, bytes)
    assert isinstance(actual.value, BaseHexBytes)


def test_invalid_hexbytes():
    with pytest.raises(ValidationError):
        Model(value="foo")


def test_fromhex(bytes32str):
    actual_with_0x = HexBytes.fromhex(bytes32str)
    actual_without_0x = HexBytes.fromhex(bytes32str[2:])
    expected = HexBytes(bytes32str)
    assert actual_with_0x == actual_without_0x == expected


def test_schema():
    actual = Model.model_json_schema()
    for name, prop in actual["properties"].items():
        assert prop["type"] == "string"
        assert prop["format"] == "binary"


def test_model_dump(bytes32str):
    model = Model(value=bytes32str)
    actual = model.model_dump()
    expected = {"value": "0x9b70bd98ccb5b6434c2ead14d68d15f392435a06ff469f8d1f8cf38b2ae0b0e2"}
    assert actual == expected
