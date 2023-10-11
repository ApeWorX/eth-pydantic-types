from typing import Any, Callable

from pydantic_core import PydanticCustomError

# NOTE: We use the factory approach because PydanticCustomError is a final class.
#   That is also why this module is internal.


def EthPydanticTypesException(fn: Callable, invalid_tag: str, **kwargs):
    return PydanticCustomError(fn.__name__, f"Invalid {invalid_tag}", kwargs)


def HexValueError(value: Any):
    return EthPydanticTypesException(HexValueError, "hex value", value=value)


def SizeError(size: Any, value: Any):
    return EthPydanticTypesException(SizeError, "size of value", value=value)
