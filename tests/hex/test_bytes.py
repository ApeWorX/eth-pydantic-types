from typing import ClassVar

import pytest
from eth_utils import to_hex
from hexbytes import HexBytes as BaseHexBytes
from pydantic import BaseModel, ValidationError, field_validator

from eth_pydantic_types.hex import BoundHexBytes, HexBytes, HexBytes32
from eth_pydantic_types.hex.bytes import HexBytes20
from eth_pydantic_types.utils import PadDirection


class BytesModel(BaseModel):
    value: HexBytes


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


class TestHexBytes32:
    def test_fromhex(self, bytes32str):
        actual_with_0x = HexBytes32.fromhex(bytes32str)
        actual_without_0x = HexBytes32.fromhex(bytes32str[2:])
        expected = HexBytes(bytes32str)
        assert actual_with_0x == actual_without_0x == expected

    def test_is_bytes(self, bytes32str):
        assert isinstance(HexBytes32.fromhex(bytes32str), bytes)


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

    def test_right_pad(self):
        class MyModel(BaseModel):
            my_bytes: HexBytes20

            @field_validator("my_bytes", mode="before")
            @classmethod
            def validate_value(cls, value, info):
                return HexBytes20.__eth_pydantic_validate__(value, pad=PadDirection.RIGHT)

        model = MyModel(my_bytes=1)
        assert model.my_bytes.startswith(HexBytes(1))
