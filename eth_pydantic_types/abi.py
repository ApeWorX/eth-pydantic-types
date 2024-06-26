"""
These models are used to match the lowercase type names used by the abi.
"""

from typing import ClassVar

from pydantic_core.core_schema import CoreSchema, str_schema

from .address import Address
from .hex import _make_cls as _make_hex_cls
from .numbers import _make_cls as _make_number_cls

bytes1 = _make_hex_cls(1, bytes, dict_additions=dict(abi_type="bytes1"))
bytes4 = _make_hex_cls(4, bytes, dict_additions=dict(abi_type="bytes4"))
bytes8 = _make_hex_cls(8, bytes, dict_additions=dict(abi_type="bytes8"))
bytes16 = _make_hex_cls(16, bytes, dict_additions=dict(abi_type="bytes16"))
bytes20 = _make_hex_cls(20, bytes, dict_additions=dict(abi_type="bytes20"))
bytes32 = _make_hex_cls(32, bytes, dict_additions=dict(abi_type="bytes32"))
bytes64 = _make_hex_cls(64, bytes, dict_additions=dict(abi_type="bytes64"))


class string(str):
    """
    Represents a string.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, value, handler=None) -> CoreSchema:
        return str_schema()

    abi_type: ClassVar[str] = "string"


class address(Address):
    """
    Represents a 20 character hex string address.
    """

    abi_type: ClassVar[str] = "address"


int8 = _make_number_cls(8, int, dict_additions=dict(abi_type="int8"))
int16 = _make_number_cls(16, int, dict_additions=dict(abi_type="int16"))
int24 = _make_number_cls(24, int, dict_additions=dict(abi_type="int24"))
int32 = _make_number_cls(32, int, dict_additions=dict(abi_type="int32"))
int40 = _make_number_cls(40, int, dict_additions=dict(abi_type="int40"))
int48 = _make_number_cls(48, int, dict_additions=dict(abi_type="int48"))
int56 = _make_number_cls(56, int, dict_additions=dict(abi_type="int56"))
int64 = _make_number_cls(64, int, dict_additions=dict(abi_type="int64"))
int72 = _make_number_cls(72, int, dict_additions=dict(abi_type="int72"))
int80 = _make_number_cls(80, int, dict_additions=dict(abi_type="int80"))
int88 = _make_number_cls(88, int, dict_additions=dict(abi_type="int88"))
int96 = _make_number_cls(96, int, dict_additions=dict(abi_type="int96"))
int104 = _make_number_cls(104, int, dict_additions=dict(abi_type="int104"))
int112 = _make_number_cls(112, int, dict_additions=dict(abi_type="int112"))
int120 = _make_number_cls(120, int, dict_additions=dict(abi_type="int120"))
int128 = _make_number_cls(128, int, dict_additions=dict(abi_type="int128"))
int136 = _make_number_cls(136, int, dict_additions=dict(abi_type="int136"))
int144 = _make_number_cls(144, int, dict_additions=dict(abi_type="int144"))
int152 = _make_number_cls(152, int, dict_additions=dict(abi_type="int152"))
int160 = _make_number_cls(160, int, dict_additions=dict(abi_type="int160"))
int168 = _make_number_cls(168, int, dict_additions=dict(abi_type="int168"))
int176 = _make_number_cls(176, int, dict_additions=dict(abi_type="int176"))
int184 = _make_number_cls(184, int, dict_additions=dict(abi_type="int184"))
int192 = _make_number_cls(192, int, dict_additions=dict(abi_type="int192"))
int200 = _make_number_cls(200, int, dict_additions=dict(abi_type="int200"))
int208 = _make_number_cls(208, int, dict_additions=dict(abi_type="int208"))
int216 = _make_number_cls(216, int, dict_additions=dict(abi_type="int216"))
int224 = _make_number_cls(224, int, dict_additions=dict(abi_type="int224"))
int232 = _make_number_cls(232, int, dict_additions=dict(abi_type="int232"))
int240 = _make_number_cls(240, int, dict_additions=dict(abi_type="int240"))
int248 = _make_number_cls(248, int, dict_additions=dict(abi_type="int248"))
int256 = _make_number_cls(256, int, dict_additions=dict(abi_type="int256"))
uint8 = _make_number_cls(8, int, signed=False, dict_additions=dict(abi_type="uint8"))
uint16 = _make_number_cls(16, int, signed=False, dict_additions=dict(abi_type="uint16"))
uint24 = _make_number_cls(24, int, signed=False, dict_additions=dict(abi_type="uint24"))
uint32 = _make_number_cls(32, int, signed=False, dict_additions=dict(abi_type="uint32"))
uint40 = _make_number_cls(40, int, signed=False, dict_additions=dict(abi_type="uint40"))
uint48 = _make_number_cls(48, int, signed=False, dict_additions=dict(abi_type="uint48"))
uint56 = _make_number_cls(56, int, signed=False, dict_additions=dict(abi_type="uint56"))
uint64 = _make_number_cls(64, int, signed=False, dict_additions=dict(abi_type="uint64"))
uint72 = _make_number_cls(72, int, signed=False, dict_additions=dict(abi_type="uint72"))
uint80 = _make_number_cls(80, int, signed=False, dict_additions=dict(abi_type="uint80"))
uint88 = _make_number_cls(88, int, signed=False, dict_additions=dict(abi_type="uint88"))
uint96 = _make_number_cls(96, int, signed=False, dict_additions=dict(abi_type="uint96"))
uint104 = _make_number_cls(104, int, signed=False, dict_additions=dict(abi_type="uint104"))
uint112 = _make_number_cls(112, int, signed=False, dict_additions=dict(abi_type="uint112"))
uint120 = _make_number_cls(120, int, signed=False, dict_additions=dict(abi_type="uint120"))
uint128 = _make_number_cls(128, int, signed=False, dict_additions=dict(abi_type="uint128"))
uint136 = _make_number_cls(136, int, signed=False, dict_additions=dict(abi_type="uint136"))
uint144 = _make_number_cls(144, int, signed=False, dict_additions=dict(abi_type="uint144"))
uint152 = _make_number_cls(152, int, signed=False, dict_additions=dict(abi_type="uint152"))
uint160 = _make_number_cls(160, int, signed=False, dict_additions=dict(abi_type="uint160"))
uint168 = _make_number_cls(168, int, signed=False, dict_additions=dict(abi_type="uint168"))
uint176 = _make_number_cls(176, int, signed=False, dict_additions=dict(abi_type="uint176"))
uint184 = _make_number_cls(184, int, signed=False, dict_additions=dict(abi_type="uint184"))
uint192 = _make_number_cls(192, int, signed=False, dict_additions=dict(abi_type="uint192"))
uint200 = _make_number_cls(200, int, signed=False, dict_additions=dict(abi_type="uint200"))
uint208 = _make_number_cls(208, int, signed=False, dict_additions=dict(abi_type="uint208"))
uint216 = _make_number_cls(216, int, signed=False, dict_additions=dict(abi_type="uint216"))
uint224 = _make_number_cls(224, int, signed=False, dict_additions=dict(abi_type="uint224"))
uint232 = _make_number_cls(232, int, signed=False, dict_additions=dict(abi_type="uint232"))
uint240 = _make_number_cls(240, int, signed=False, dict_additions=dict(abi_type="uint240"))
uint248 = _make_number_cls(248, int, signed=False, dict_additions=dict(abi_type="uint248"))
uint256 = _make_number_cls(256, int, signed=False, dict_additions=dict(abi_type="uint256"))
