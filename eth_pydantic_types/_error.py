from typing import Any, Callable

from pydantic_core import PydanticCustomError

# NOTE: We use the factory approach because PydanticCustomError is a final class.
#   That is also why this module is internal.


def CustomError(fn: Callable, invalid_tag: str, **kwargs) -> PydanticCustomError:
    return PydanticCustomError(fn.__name__, f"Invalid {invalid_tag}", kwargs)


def HexValueError(value: Any) -> PydanticCustomError:
    return CustomError(HexValueError, "hex value", value=value)


def SizeError(size: Any, value: Any) -> PydanticCustomError:
    return CustomError(SizeError, "size of value", size=size, value=value)


def Bip122UriFormatError(value: str) -> PydanticCustomError:
    return CustomError(
        Bip122UriFormatError,
        "BIP-122 URI format",
        uri=value,
        format="blockchain://<genesis_hash>/block/<block_hash>.",
    )
