from typing_extensions import assert_type

from eth_pydantic_types.hex.bytes import HexBytes32


def test_hexbytes_fromhex():
    x = HexBytes32.fromhex("00" * 32)
    assert_type(x, HexBytes32)
    assert isinstance(x, HexBytes32)
