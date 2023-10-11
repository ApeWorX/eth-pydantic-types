import pytest
from hexbytes import HexBytes as BaseHexBytes
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hex import HexBytes, HexStr


class BytesModel(BaseModel):
    value: HexBytes


class StrModel(BaseModel):
    value: HexStr


@pytest.mark.parametrize("value", ("0xa", 10, b"\n"))
def test_hexbytes(value):
    actual = BytesModel(value=value)

    # The end result, the value is a hexbytes.HexBytes
    assert actual.value == BaseHexBytes(value)
    assert actual.value.hex() == "0x0a"
    assert isinstance(actual.value, bytes)
    assert isinstance(actual.value, BaseHexBytes)


def test_invalid_hexbytes():
    with pytest.raises(ValidationError):
        BytesModel(value="foo")


def test_hexbytes_fromhex(bytes32str):
    actual_with_0x = HexBytes.fromhex(bytes32str)
    actual_without_0x = HexBytes.fromhex(bytes32str[2:])
    expected = HexBytes(bytes32str)
    assert actual_with_0x == actual_without_0x == expected


def test_hexbytes_schema():
    actual = BytesModel.model_json_schema()
    prop = actual["properties"]["value"]
    assert prop["type"] == "string"
    assert prop["format"] == "binary"
    assert prop["pattern"] == "^0x([0-9a-f][0-9a-f])*$"
    assert prop["examples"] == [
        "0x",
        "0xd4",
        "0xd4e5",
        "0xd4e56740",
        "0xd4e56740f876aef8",
        "0xd4e56740f876aef8c010b86a40d5f567",
        "0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3",
    ]


def test_hexbytes_model_dump(bytes32str):
    model = BytesModel(value=bytes32str)
    actual = model.model_dump()
    expected = {"value": "0x9b70bd98ccb5b6434c2ead14d68d15f392435a06ff469f8d1f8cf38b2ae0b0e2"}
    assert actual == expected


@pytest.mark.parametrize("value", ("0xa", 10, HexBytes(10)))
def test_hexstr(value):
    actual = StrModel(value=value)

    # The end result, the value is a str
    assert actual.value == "0x0a"
    assert isinstance(actual.value, str)


def test_invalid_hexstr():
    with pytest.raises(ValidationError):
        StrModel(value="foo")


def test_hexstr_conversions():
    model = StrModel(value="0x123")
    assert int(model.value, 16) == 291
    assert bytes.fromhex(model.value[2:]) == b"\x01#"


def test_hexstr_schema():
    actual = StrModel.model_json_schema()
    properties = actual["properties"]
    assert len(properties) == 1
    prop = properties["value"]
    assert prop["type"] == "string"
    assert prop["format"] == "binary"
    assert prop["pattern"] == "^0x([0-9a-f][0-9a-f])*$"
    assert prop["examples"] == [
        "0x",
        "0xd4",
        "0xd4e5",
        "0xd4e56740",
        "0xd4e56740f876aef8",
        "0xd4e56740f876aef8c010b86a40d5f567",
        "0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3",
    ]


def test_hexstr_model_dump(bytes32str):
    model = StrModel(value=bytes32str)
    actual = model.model_dump()
    expected = {"value": "0x9b70bd98ccb5b6434c2ead14d68d15f392435a06ff469f8d1f8cf38b2ae0b0e2"}
    assert actual == expected

    model = StrModel(value=3)
    actual = model.model_dump()
    expected = {"value": "0x03"}
    assert actual == expected
