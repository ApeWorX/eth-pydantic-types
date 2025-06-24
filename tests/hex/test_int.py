from typing import ClassVar

import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.hex import (
    BoundHexInt,
    HexInt,
)


class IntModel(BaseModel):
    value: HexInt


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
