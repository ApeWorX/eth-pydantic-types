"""
These models are used to match the lowercase type names used by the abi.
"""

from typing import ClassVar

from pydantic import Field
from typing_extensions import Annotated, TypeAliasType

from .address import Address
from .hex import BoundHexBytes, HexBytes

bytes = TypeAliasType("bytes", HexBytes)
string = TypeAliasType("string", str)
address = TypeAliasType("address", Address)


class bytes1(BoundHexBytes):
    size: ClassVar[int] = 1


class bytes2(BoundHexBytes):
    size: ClassVar[int] = 2


class bytes3(BoundHexBytes):
    size: ClassVar[int] = 3


class bytes4(BoundHexBytes):
    size: ClassVar[int] = 4


class bytes5(BoundHexBytes):
    size: ClassVar[int] = 5


class bytes6(BoundHexBytes):
    size: ClassVar[int] = 6


class bytes7(BoundHexBytes):
    size: ClassVar[int] = 7


class bytes8(BoundHexBytes):
    size: ClassVar[int] = 8


class bytes9(BoundHexBytes):
    size: ClassVar[int] = 9


class bytes10(BoundHexBytes):
    size: ClassVar[int] = 10


class bytes11(BoundHexBytes):
    size: ClassVar[int] = 11


class bytes12(BoundHexBytes):
    size: ClassVar[int] = 12


class bytes13(BoundHexBytes):
    size: ClassVar[int] = 13


class bytes14(BoundHexBytes):
    size: ClassVar[int] = 14


class bytes15(BoundHexBytes):
    size: ClassVar[int] = 15


class bytes16(BoundHexBytes):
    size: ClassVar[int] = 16


class bytes17(BoundHexBytes):
    size: ClassVar[int] = 17


class bytes18(BoundHexBytes):
    size: ClassVar[int] = 18


class bytes19(BoundHexBytes):
    size: ClassVar[int] = 19


class bytes20(BoundHexBytes):
    size: ClassVar[int] = 20


class bytes21(BoundHexBytes):
    size: ClassVar[int] = 21


class bytes22(BoundHexBytes):
    size: ClassVar[int] = 22


class bytes23(BoundHexBytes):
    size: ClassVar[int] = 23


class bytes24(BoundHexBytes):
    size: ClassVar[int] = 24


class bytes25(BoundHexBytes):
    size: ClassVar[int] = 25


class bytes26(BoundHexBytes):
    size: ClassVar[int] = 26


class bytes27(BoundHexBytes):
    size: ClassVar[int] = 27


class bytes28(BoundHexBytes):
    size: ClassVar[int] = 28


class bytes29(BoundHexBytes):
    size: ClassVar[int] = 29


class bytes30(BoundHexBytes):
    size: ClassVar[int] = 30


class bytes31(BoundHexBytes):
    size: ClassVar[int] = 31


class bytes32(BoundHexBytes):
    size: ClassVar[int] = 32


int8 = TypeAliasType("int8", Annotated[int, Field(lt=2**7, ge=-(2**7))])
int16 = TypeAliasType("int16", Annotated[int, Field(lt=2**15, ge=-(2**15))])
int24 = TypeAliasType("int24", Annotated[int, Field(lt=2**23, ge=-(2**23))])
int32 = TypeAliasType("int32", Annotated[int, Field(lt=2**31, ge=-(2**31))])
int40 = TypeAliasType("int40", Annotated[int, Field(lt=2**39, ge=-(2**39))])
int48 = TypeAliasType("int48", Annotated[int, Field(lt=2**47, ge=-(2**47))])
int56 = TypeAliasType("int56", Annotated[int, Field(lt=2**55, ge=-(2**55))])
int64 = TypeAliasType("int64", Annotated[int, Field(lt=2**63, ge=-(2**63))])
int72 = TypeAliasType("int72", Annotated[int, Field(lt=2**71, ge=-(2**71))])
int80 = TypeAliasType("int80", Annotated[int, Field(lt=2**79, ge=-(2**79))])
int88 = TypeAliasType("int88", Annotated[int, Field(lt=2**87, ge=-(2**87))])
int96 = TypeAliasType("int96", Annotated[int, Field(lt=2**95, ge=-(2**95))])
int104 = TypeAliasType("int104", Annotated[int, Field(lt=2**103, ge=-(2**103))])
int112 = TypeAliasType("int112", Annotated[int, Field(lt=2**111, ge=-(2**111))])
int120 = TypeAliasType("int120", Annotated[int, Field(lt=2**119, ge=-(2**119))])
int128 = TypeAliasType("int128", Annotated[int, Field(lt=2**127, ge=-(2**127))])
int136 = TypeAliasType("int136", Annotated[int, Field(lt=2**135, ge=-(2**135))])
int144 = TypeAliasType("int144", Annotated[int, Field(lt=2**143, ge=-(2**143))])
int152 = TypeAliasType("int152", Annotated[int, Field(lt=2**151, ge=-(2**151))])
int160 = TypeAliasType("int160", Annotated[int, Field(lt=2**159, ge=-(2**159))])
int168 = TypeAliasType("int168", Annotated[int, Field(lt=2**167, ge=-(2**167))])
int176 = TypeAliasType("int176", Annotated[int, Field(lt=2**175, ge=-(2**175))])
int184 = TypeAliasType("int184", Annotated[int, Field(lt=2**183, ge=-(2**183))])
int192 = TypeAliasType("int192", Annotated[int, Field(lt=2**191, ge=-(2**191))])
int200 = TypeAliasType("int200", Annotated[int, Field(lt=2**199, ge=-(2**199))])
int208 = TypeAliasType("int208", Annotated[int, Field(lt=2**207, ge=-(2**207))])
int216 = TypeAliasType("int216", Annotated[int, Field(lt=2**215, ge=-(2**215))])
int224 = TypeAliasType("int224", Annotated[int, Field(lt=2**223, ge=-(2**223))])
int232 = TypeAliasType("int232", Annotated[int, Field(lt=2**231, ge=-(2**231))])
int240 = TypeAliasType("int240", Annotated[int, Field(lt=2**239, ge=-(2**239))])
int248 = TypeAliasType("int248", Annotated[int, Field(lt=2**247, ge=-(2**247))])
int256 = TypeAliasType("int256", Annotated[int, Field(lt=2**255, ge=-(2**255))])
uint8 = TypeAliasType("uint8", Annotated[int, Field(lt=2**8, ge=0)])
uint16 = TypeAliasType("uint16", Annotated[int, Field(lt=2**16, ge=0)])
uint24 = TypeAliasType("uint24", Annotated[int, Field(lt=2**24, ge=0)])
uint32 = TypeAliasType("uint32", Annotated[int, Field(lt=2**32, ge=0)])
uint40 = TypeAliasType("uint40", Annotated[int, Field(lt=2**40, ge=0)])
uint48 = TypeAliasType("uint48", Annotated[int, Field(lt=2**48, ge=0)])
uint56 = TypeAliasType("uint56", Annotated[int, Field(lt=2**56, ge=0)])
uint64 = TypeAliasType("uint64", Annotated[int, Field(lt=2**64, ge=0)])
uint72 = TypeAliasType("uint72", Annotated[int, Field(lt=2**72, ge=0)])
uint80 = TypeAliasType("uint80", Annotated[int, Field(lt=2**80, ge=0)])
uint88 = TypeAliasType("uint88", Annotated[int, Field(lt=2**88, ge=0)])
uint96 = TypeAliasType("uint96", Annotated[int, Field(lt=2**96, ge=0)])
uint104 = TypeAliasType("uint104", Annotated[int, Field(lt=2**104, ge=0)])
uint112 = TypeAliasType("uint112", Annotated[int, Field(lt=2**112, ge=0)])
uint120 = TypeAliasType("uint120", Annotated[int, Field(lt=2**120, ge=0)])
uint128 = TypeAliasType("uint128", Annotated[int, Field(lt=2**128, ge=0)])
uint136 = TypeAliasType("uint136", Annotated[int, Field(lt=2**136, ge=0)])
uint144 = TypeAliasType("uint144", Annotated[int, Field(lt=2**144, ge=0)])
uint152 = TypeAliasType("uint152", Annotated[int, Field(lt=2**152, ge=0)])
uint160 = TypeAliasType("uint160", Annotated[int, Field(lt=2**160, ge=0)])
uint168 = TypeAliasType("uint168", Annotated[int, Field(lt=2**168, ge=0)])
uint176 = TypeAliasType("uint176", Annotated[int, Field(lt=2**176, ge=0)])
uint184 = TypeAliasType("uint184", Annotated[int, Field(lt=2**184, ge=0)])
uint192 = TypeAliasType("uint192", Annotated[int, Field(lt=2**192, ge=0)])
uint200 = TypeAliasType("uint200", Annotated[int, Field(lt=2**200, ge=0)])
uint208 = TypeAliasType("uint208", Annotated[int, Field(lt=2**208, ge=0)])
uint216 = TypeAliasType("uint216", Annotated[int, Field(lt=2**216, ge=0)])
uint224 = TypeAliasType("uint224", Annotated[int, Field(lt=2**224, ge=0)])
uint232 = TypeAliasType("uint232", Annotated[int, Field(lt=2**232, ge=0)])
uint240 = TypeAliasType("uint240", Annotated[int, Field(lt=2**240, ge=0)])
uint248 = TypeAliasType("uint248", Annotated[int, Field(lt=2**248, ge=0)])
uint256 = TypeAliasType("uint256", Annotated[int, Field(lt=2**256, ge=0)])
