from typing import Union

from pydantic_core.core_schema import plain_serializer_function_ser_schema


def serialize_hex(value: Union[int, bytes]) -> str:
    hex_value = value.hex() if isinstance(value, bytes) else hex(value)
    hex_value = hex_value[2:] if hex_value.startswith("0x") else hex_value

    # Ensure even number of left-padded zeroes.
    if len(hex_value) % 2 != 0:
        hex_value = f"0{hex_value}"

    return f"0x{hex_value}"


hex_serializer = plain_serializer_function_ser_schema(function=serialize_hex)
