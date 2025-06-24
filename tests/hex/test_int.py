from typing import ClassVar

import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hex import (
    BoundHexInt,
    HexInt,
    HexInt32,
    UInt256,
)
from eth_pydantic_types.hex.bytes import HexBytes


class IntModel(BaseModel):
    value: HexInt


class HexInt32Model(BaseModel):
    value: HexInt32


class UInt256Model(BaseModel):
    value: UInt256


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

    @pytest.mark.parametrize("value", (-1, 2 * 8**256))
    def test_out_of_bounds(self, value):
        class PublicKey(BoundHexInt):
            size: ClassVar[int] = 64
            signed: ClassVar[bool] = False

        class Model(BaseModel):
            pub_key: PublicKey

        with pytest.raises(ValidationError):
            _ = Model(pub_key=value)


class TestHexInt32:
    @pytest.mark.parametrize("value", ("0xa", 10, b"\n"))
    def test_valid(self, value):
        actual = HexInt32Model(value=value)
        assert actual.value == 10

        str_value = actual.model_dump()["value"]
        expected = "0x000000000000000000000000000000000000000000000000000000000000000a"
        assert str_value == expected

        # The resulting size in bytes is 32.
        assert len(HexBytes(str_value)) == 32


# Even though UInt256 is a TypeAlias of HexInt32, we want to ensure it functions separately.
class TestUInt256:
    @pytest.mark.parametrize("value", ("0xa", 10, b"\n"))
    def test_valid(self, value):
        actual = UInt256Model(value=value)
        assert actual.value == 10

        str_value = actual.model_dump()["value"]
        expected = "0x000000000000000000000000000000000000000000000000000000000000000a"
        assert str_value == expected

        # The resulting size in bytes is 32.
        assert len(HexBytes(str_value)) == 32


def test_custom_type():
    # An 8-byte unsigned hex integer.
    class NetworkID(BoundHexInt):
        size: int = 8
        signed: bool = False

    class MyModel(BaseModel):
        network_id: NetworkID

    # Sepolia.
    model = MyModel(network_id=11155111)
    assert model.network_id == 11155111

    model_json = model.model_dump_json()
    assert model_json == '{"network_id":"0x0000000000aa36a7"}'
