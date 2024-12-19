import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hex import HexBytes, HexBytes20, HexBytes32, HexStr32


class Model(BaseModel):
    valuebytes20: HexBytes20
    valuebytes32: HexBytes32
    valuestr32: HexStr32

    @classmethod
    def from_single(cls, value):
        return cls(
            valuebytes20=value,
            valuebytes32=value,
            valuestr32=value,
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
    assert len(model.valuebytes20) == 20
    assert len(model.valuebytes32) == 32
    assert len(model.valuestr32) == 66
    assert model.valuebytes20.hex().endswith("32")
    assert model.valuebytes32.hex().endswith("32")
    assert model.valuestr32.endswith("32")


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
        "valuebytes20": "0x0000000000000000000000000000000000000005",
        "valuebytes32": "0x0000000000000000000000000000000000000000000000000000000000000005",
        "valuestr32": "0x0000000000000000000000000000000000000000000000000000000000000005",
    }
    assert actual == expected
