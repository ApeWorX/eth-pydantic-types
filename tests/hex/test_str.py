import pytest
from pydantic import BaseModel, ValidationError, field_validator

from eth_pydantic_types.hex import (
    HexBytes,
    HexStr,
    HexStr20,
)
from eth_pydantic_types.utils import PadDirection


class StrModel(BaseModel):
    value: HexStr


class TestHexStr:
    @pytest.mark.parametrize("value", ("0xa", 10, HexBytes(10)))
    def test_valid(self, value):
        actual = StrModel(value=value)

        # The end result, the value is a str
        assert actual.value == "0x0a"
        assert isinstance(actual.value, str)

    def test_invalid(self):
        with pytest.raises(ValidationError):
            StrModel(value="foo")

    def test_conversions(self):
        model = StrModel(value="0x123")
        assert int(model.value, 16) == 291
        assert bytes.fromhex(model.value[2:]) == b"\x01#"

    def test_schema(self):
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

    def test_model_dump(self, bytes32str):
        model = StrModel(value=bytes32str)
        actual = model.model_dump()
        expected = {"value": "0x9b70bd98ccb5b6434c2ead14d68d15f392435a06ff469f8d1f8cf38b2ae0b0e2"}
        assert actual == expected

        model = StrModel(value=3)
        actual = model.model_dump()
        expected = {"value": "0x03"}
        assert actual == expected

    def test_from_bytes(self):
        value = b"\xb7\xfc\xef\x7f\xe7E\xf2\xa9U`\xff_U\x0e;\x8f"
        actual = HexStr.from_bytes(value)
        assert actual.startswith("0x")

    def test_hex_removes_leading_zeroes_if_needed(self):
        address = "0x000000000000000000000000cafac3dd18ac6c6e92c921884f9e4176737c052c"

        class MyModel(BaseModel):
            my_address: HexStr20

        # Test both str and bytes for input.
        for addr in (address, HexBytes(address)):
            model = MyModel(my_address=addr)
            assert len(model.my_address) == 42
            assert model.my_address == "0xcafac3dd18ac6c6e92c921884f9e4176737c052c"

        def test_from_bytes(self):
            value = b"\x101\xf0\xc9\xacT\xdc\xb6KO\x12\x1a'\x95|\x14&<\\\xb4"
            model = StrModel(value=value)
            assert model.value == HexBytes(value)

    def test_right_pad(self):
        class MyModel(BaseModel):
            my_str: HexStr20

            @field_validator("my_str", mode="before")
            @classmethod
            def validate_value(cls, value, info):
                field_type = cls.model_fields[info.field_name].annotation
                assert field_type  # For Mypy
                return field_type.__eth_pydantic_validate__(value, pad=PadDirection.RIGHT)

        model = MyModel(my_str=1)
        assert model.my_str.startswith("0x01")
