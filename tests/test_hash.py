import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hex import (
    HexBytes,
    HexBytes8,
    HexBytes16,
    HexBytes20,
    HexBytes32,
    HexBytes64,
    HexStr8,
    HexStr16,
    HexStr32,
    HexStr64,
)


class Model(BaseModel):
    valuebytes8: HexBytes8
    valuebytes16: HexBytes16
    valuebytes20: HexBytes20
    valuebytes32: HexBytes32
    valuebytes64: HexBytes64
    valuestr8: HexStr8
    valuestr16: HexStr16
    valuestr32: HexStr32
    valuestr64: HexStr64

    @classmethod
    def from_single(cls, value):
        return cls(
            valuebytes8=value,
            valuebytes16=value,
            valuebytes20=value,
            valuebytes32=value,
            valuebytes64=value,
            valuestr8=value,
            valuestr16=value,
            valuestr32=value,
            valuestr64=value,
        )


def test_hashbytes_fromhex(bytes32str):
    actual_with_0x = HexBytes32.fromhex(bytes32str)
    actual_without_0x = HexBytes32.fromhex(bytes32str[2:])
    expected = HexBytes(bytes32str)
    assert actual_with_0x == actual_without_0x == expected


def test_hashbytes_is_bytes(bytes32str):
    assert isinstance(HexBytes32.fromhex(bytes32str), bytes)


@pytest.mark.parametrize("value", ("0x32", HexBytes("0x32"), b"2", 50))
def test_hash(value):
    model = Model.from_single(value)
    assert len(model.valuebytes8) == 8
    assert len(model.valuebytes16) == 16
    assert len(model.valuebytes20) == 20
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


def test_hash_removes_leading_zeroes_if_needed():
    address = "0x000000000000000000000000cafac3dd18ac6c6e92c921884f9e4176737c052c"

    class MyModel(BaseModel):
        my_address: HexBytes20

    # Test both str and bytes for input.
    for addr in (address, HexBytes(address)):
        model = MyModel(my_address=addr)
        assert len(model.my_address) == 20
        assert model.my_address == HexBytes("0xcafac3dd18ac6c6e92c921884f9e4176737c052c")


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
        "valuebytes8": "0000000000000005",
        "valuestr8": "0x0000000000000005",
        "valuebytes16": "00000000000000000000000000000005",
        "valuebytes20": "0000000000000000000000000000000000000005",
        "valuestr16": "0x00000000000000000000000000000005",
        "valuebytes32": "0000000000000000000000000000000000000000000000000000000000000005",
        "valuestr32": "0x0000000000000000000000000000000000000000000000000000000000000005",
        "valuebytes64": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005",  # noqa: E501
        "valuestr64": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005",  # noqa: E501
    }
    assert actual == expected
