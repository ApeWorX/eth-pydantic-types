from pydantic import BaseModel
from pydantic_core.core_schema import str_schema, with_info_before_validator_function

from eth_pydantic_types import HexStr32


class MyAddress(HexStr32):
    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None):
        str_size = cls.size * 2
        return with_info_before_validator_function(
            cls.__eth_pydantic_validate__,
            str_schema(max_length=str_size, min_length=str_size),
        )

    @classmethod
    def __eth_pydantic_validate__(cls, value, info=None, **kwargs):
        return super().__eth_pydantic_validate__(value, info=info, prefixed=False, **kwargs)


class MyModel(BaseModel):
    address: MyAddress


class TestCustomTypes:
    def test_unprefixed_from_str(self):
        model = MyModel(address="0x" + "ab" * 32)
        assert not model.address.startswith("0x")
        assert len(model.address) == 64

    def test_unprefixed_from_bytes(self):
        model = MyModel(address=b"\xab" * 32)
        assert not model.address.startswith("0x")
        assert len(model.address) == 64

    def test_unprefixed_from_int(self):
        model = MyModel(address=123)
        assert not model.address.startswith("0x")
        assert len(model.address) == 64
