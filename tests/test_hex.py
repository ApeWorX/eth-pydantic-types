from typing import ClassVar

import pytest
from eth_utils import to_hex
from hexbytes import HexBytes as BaseHexBytes
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hex import (
    BoundHexBytes,
    BoundHexInt,
    HexBytes,
    HexBytes20,
    HexBytes32,
    HexInt,
    HexStr,
    HexStr20,
    HexStr32,
)


class BytesModel(BaseModel):
    value: HexBytes


class StrModel(BaseModel):
    value: HexStr


class IntModel(BaseModel):
    value: HexInt


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


class TestHexBytes:
    @pytest.mark.parametrize("value", ("0xa", 10, b"\n"))
    def test_valid(self, value):
        actual = BytesModel(value=value)

        # The end result, the value is a hexbytes.HexBytes
        assert actual.value == BaseHexBytes(value)
        assert to_hex(actual.value) == "0x0a"
        assert isinstance(actual.value, bytes)
        assert isinstance(actual.value, BaseHexBytes)

    def test_invalid(self):
        with pytest.raises(ValidationError):
            BytesModel(value="foo")

    def test_fromhex(self, bytes32str):
        actual_with_0x = HexBytes.fromhex(bytes32str)
        actual_without_0x = HexBytes.fromhex(bytes32str[2:])
        expected = HexBytes(bytes32str)
        assert actual_with_0x == actual_without_0x == expected

    def test_schema(self):
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

    def test_model_dump(self, bytes32str):
        model = BytesModel(value=bytes32str)
        actual = model.model_dump()
        expected = {"value": "0x9b70bd98ccb5b6434c2ead14d68d15f392435a06ff469f8d1f8cf38b2ae0b0e2"}
        assert actual == expected

    def test_from_bytes(self):
        value = b"\x101\xf0\xc9\xacT\xdc\xb6KO\x12\x1a'\x95|\x14&<\\\xb4"
        model = BytesModel(value=value)
        assert model.value == HexBytes(value)


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


class TestHexBytes32:
    def test_fromhex(self, bytes32str):
        actual_with_0x = HexBytes32.fromhex(bytes32str)
        actual_without_0x = HexBytes32.fromhex(bytes32str[2:])
        expected = HexBytes(bytes32str)
        assert actual_with_0x == actual_without_0x == expected

    def test_is_bytes(self, bytes32str):
        assert isinstance(HexBytes32.fromhex(bytes32str), bytes)


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
        assert model.valuebytes20.hex().endswith("32")
        assert model.valuebytes32.hex().endswith("32")
        assert model.valuestr32.endswith("32")

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


class TestBoundHexBytes:
    """
    Showing how to use BoundHexBytes to make your own bounded-types.
    """

    def test_use_bound_type(self):
        class PublicKey(BoundHexBytes):
            size: ClassVar[int] = 64

        class Account(BaseModel):
            pub_key: PublicKey

        key = (
            "0x000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000000000000000000005"
        )
        account = Account(pub_key=key)
        assert account.pub_key == HexBytes(key)


class TestHexInt:
    @pytest.mark.parametrize("value", ("0xa", 10, b"\n"))
    def test_valid(self, value):
        actual = IntModel(value=value)
        assert actual.value == 10

    def test_invalid(self):
        with pytest.raises(ValidationError):
            _ = IntModel(value="foo")

    def test_schema(self):
        actual = IntModel.model_json_schema()
        assert actual["properties"]["value"]["type"] == "integer"
        assert actual["properties"]["value"]["examples"][0].startswith("0x")

    def test_model_dump(self):
        model = IntModel(value=10)
        actual = model.model_dump()
        assert actual == {"value": "0x0a"}

    @pytest.mark.parametrize("value", (-1, 2**256))
    def test_out_of_bounds(self, value):
        class PublicKey(BoundHexInt):
            size: ClassVar[int] = 64
            signed: ClassVar[bool] = False

        class Model(BaseModel):
            pub_key: PublicKey

        with pytest.raises(ValidationError):
            _ = Model(pub_key=value)
