import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hex import (
    HexBytes,
    HexBytes20,
    HexBytes32,
    HexStr32,
)


class SizedModel(BaseModel):
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


class TestSized:
    """
    Testing all or any sized hex types in a pydantic model.
    """

    @pytest.mark.parametrize("value", ("0x32", HexBytes("0x32"), b"2", 50))
    def test_valid(self, value):
        model = SizedModel.from_single(value)
        assert len(model.valuebytes20) == 20
        assert len(model.valuebytes32) == 32
        assert len(model.valuestr32) == 66

        if isinstance(value, int):
            assert model.valuebytes20.hex().endswith("32")
            assert model.valuebytes32.hex().endswith("32")
            assert model.valuestr32.endswith("32")
        else:
            assert model.valuebytes20.hex().startswith("32")
            assert model.valuebytes32.hex().startswith("32")
            assert model.valuestr32.startswith("0x32")

    @pytest.mark.parametrize("value", ("foo", -35, "0x" + ("F" * 100)))
    def test_invalid_hash(self, value):
        with pytest.raises(ValidationError):
            SizedModel.from_single(value)

    def test_construct_removes_leading_zeroes_if_needed(self):
        address = "0x000000000000000000000000cafac3dd18ac6c6e92c921884f9e4176737c052c"

        class MyModel(BaseModel):
            my_address: HexBytes20

        # Test both str and bytes for input.
        for addr in (address, HexBytes(address)):
            model = MyModel(my_address=addr)
            assert len(model.my_address) == 20
            assert model.my_address == HexBytes("0xcafac3dd18ac6c6e92c921884f9e4176737c052c")

    def test_schema(self):
        actual = SizedModel.model_json_schema()
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

    def test_model_dump(self, bytes32str):
        model = SizedModel.from_single(5)
        actual = model.model_dump()
        expected = {
            "valuebytes20": "0x0000000000000000000000000000000000000005",
            "valuebytes32": "0x0000000000000000000000000000000000000000000000000000000000000005",
            "valuestr32": "0x0000000000000000000000000000000000000000000000000000000000000005",
        }
        assert actual == expected

    def test_right_versus_left_pad(self):
        class SimpleModel(BaseModel):
            valuebytes: HexBytes32
            valuestr: HexStr32

        leftpad = SimpleModel(valuebytes=5, valuestr=5)
        rightpad = SimpleModel(valuebytes="0x05", valuestr="0x05")
        assert leftpad.valuebytes == HexBytes(
            "0x0000000000000000000000000000000000000000000000000000000000000005"
        )
        assert leftpad.valuestr == (
            "0x0000000000000000000000000000000000000000000000000000000000000005"
        )
        assert rightpad.valuebytes == HexBytes(
            "0x0500000000000000000000000000000000000000000000000000000000000000"
        )
        assert rightpad.valuestr == (
            "0x0500000000000000000000000000000000000000000000000000000000000000"
        )
