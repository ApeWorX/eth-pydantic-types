import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hash import (
    HashBytes8,
    HashBytes16,
    HashBytes32,
    HashBytes64,
    HashStr8,
    HashStr16,
    HashStr32,
    HashStr64,
)
from eth_pydantic_types.hex import HexBytes


class Model(BaseModel):
    valuebytes8: HashBytes8
    valuebytes16: HashBytes16
    valuebytes32: HashBytes32
    valuebytes64: HashBytes64
    valuestr8: HashStr8
    valuestr16: HashStr16
    valuestr32: HashStr32
    valuestr64: HashStr64

    @classmethod
    def from_single(cls, value):
        return cls(
            valuebytes8=value,
            valuebytes16=value,
            valuebytes32=value,
            valuebytes64=value,
            valuestr8=value,
            valuestr16=value,
            valuestr32=value,
            valuestr64=value,
        )


def test_hashbytes_fromhex(bytes32str):
    actual_with_0x = HashBytes32.fromhex(bytes32str)
    actual_without_0x = HashBytes32.fromhex(bytes32str[2:])
    expected = HexBytes(bytes32str)
    assert actual_with_0x == actual_without_0x == expected


def test_hashbytes_is_bytes(bytes32str):
    assert isinstance(HashBytes32.fromhex(bytes32str), bytes)


@pytest.mark.parametrize("value", ("0x32", HexBytes("0x32"), b"2", 50))
def test_hash(value):
    model = Model.from_single(value)
    assert len(model.valuebytes8) == 8
    assert len(model.valuebytes16) == 16
    assert len(model.valuebytes32) == 32
    assert len(model.valuebytes64) == 64
    assert len(model.valuestr8) == 18
    assert len(model.valuestr16) == 34
    assert len(model.valuestr32) == 66
    assert len(model.valuestr64) == 130
    assert model.valuebytes8.hex().endswith("32")
    assert model.valuebytes16.hex().endswith("32")
    assert model.valuebytes32.hex().endswith("32")
    assert model.valuestr64.endswith("32")
    assert model.valuestr8.endswith("32")
    assert model.valuestr16.endswith("32")
    assert model.valuestr32.endswith("32")
    assert model.valuestr64.endswith("32")


@pytest.mark.parametrize("value", ("foo", -35, "0x" + ("F" * 100)))
def test_invalid_hash(value):
    with pytest.raises(ValidationError):
        Model.from_single(value)


def test_schema():
    actual = Model.model_json_schema()
    for name, prop in actual["properties"].items():
        is_bytes = "bytes" in name
        if is_bytes:
            size_from_name = int(name.replace("valuebytes", ""))
            expected_length = size_from_name
        else:
            size_from_name = int(name.replace("valuestr", ""))
            expected_length = size_from_name * 2 + 2

        hex_value_str_size = size_from_name * 2

        assert prop["maxLength"] == expected_length
        assert prop["minLength"] == expected_length
        assert prop["type"] == "string"
        assert prop["format"] == "binary"
        assert prop["pattern"] == f"^0x[a-fA-F0-9]{{{hex_value_str_size}}}$"

        assert prop["examples"][0] == f"0x{'0' * hex_value_str_size}"
        assert prop["examples"][1].startswith("0x0")  # Leading zero
        assert prop["examples"][2].endswith("0")  # Trailing zero
        assert all(len(ex) == hex_value_str_size + 2 for ex in prop["examples"])


def test_model_dump(bytes32str):
    model = Model.from_single(5)
    actual = model.model_dump()
    expected = {
        "valuebytes8": "0x0000000000000005",
        "valuestr8": "0x0000000000000005",
        "valuebytes16": "0x00000000000000000000000000000005",
        "valuestr16": "0x00000000000000000000000000000005",
        "valuebytes32": "0x0000000000000000000000000000000000000000000000000000000000000005",
        "valuestr32": "0x0000000000000000000000000000000000000000000000000000000000000005",
        "valuebytes64": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005",  # noqa: E501
        "valuestr64": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005",  # noqa: E501
    }
    assert actual == expected
