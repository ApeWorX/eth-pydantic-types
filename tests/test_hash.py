import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hash import Hash8, Hash16, Hash32, Hash64
from eth_pydantic_types.hexbytes import HexBytes


class Model(BaseModel):
    value8: Hash8
    value16: Hash16
    value32: Hash32
    value64: Hash64


def test_fromhex(bytes32str):
    actual_with_0x = Hash32.fromhex(bytes32str)
    actual_without_0x = Hash32.fromhex(bytes32str[2:])
    expected = HexBytes(bytes32str)
    assert actual_with_0x == actual_without_0x == expected


def test_hash_is_bytes(bytes32str):
    assert isinstance(Hash32.fromhex(bytes32str), bytes)


@pytest.mark.parametrize("value", ("0x32", HexBytes("0x32"), b"2", 50))
def test_hash(value):
    model = Model(value8=value, value16=value, value32=value, value64=value)
    assert len(model.value8) == 8
    assert len(model.value16) == 16
    assert len(model.value32) == 32
    assert len(model.value64) == 64
    assert model.value8.hex().endswith("32")
    assert model.value16.hex().endswith("32")
    assert model.value32.hex().endswith("32")
    assert model.value64.hex().endswith("32")


@pytest.mark.parametrize("value", ("foo", -35, "0x" + ("F" * 100)))
def test_invalid_hash(value):
    with pytest.raises(ValidationError):
        Model(value8=value, value16=value, value32=value, value64=value)


def test_schema():
    actual = Model.model_json_schema()
    for name, prop in actual["properties"].items():
        size_from_name = int(name.replace("value", ""))
        assert prop["maxLength"] == size_from_name
        assert prop["minLength"] == size_from_name
        assert prop["type"] == "string"
        assert prop["format"] == "binary"


def test_model_dump(bytes32str):
    model = Model(value8=5, value16=5, value32=5, value64=5)
    actual = model.model_dump()
    expected = {
        "value16": "0x00000000000000000000000000000005",
        "value32": "0x0000000000000000000000000000000000000000000000000000000000000005",
        "value64": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005",  # noqa: E501
        "value8": "0x0000000000000005",
    }
    assert actual == expected
