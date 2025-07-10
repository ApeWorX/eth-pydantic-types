from typing import Optional, Union

from pydantic_core.core_schema import plain_serializer_function_ser_schema

from eth_pydantic_types.utils import PadDirection, validate_str_size


def serialize_hex(
    value: Union[int, bytes],
    size: Optional[int] = None,
    pad: Optional[PadDirection] = None,
    force_even_length: Optional[bool] = None,
) -> str:
    hex_value = value.hex() if isinstance(value, bytes) else hex(value)
    hex_value = hex_value[2:] if hex_value.startswith("0x") else hex_value

    if pad is not None and force_even_length is not None:
        # If padding at all and force_even_length not specified, assume True.
        force_even_length = True

    # Ensure even number of left-padded zeroes.
    if force_even_length and len(hex_value) % 2 != 0:
        hex_value = f"0{hex_value}"

    if size is not None and pad is not None:
        hex_value = validate_str_size(hex_value, size * 2, pad_direction=pad)

    return f"0x{hex_value}"


def create_hex_serializer(
    size: Optional[int] = None,
    pad: Optional[PadDirection] = None,
    force_even_length: Optional[bool] = None,
):
    return plain_serializer_function_ser_schema(
        function=lambda value: serialize_hex(
            value, size=size, pad=pad, force_even_length=force_even_length
        )
    )


hex_serializer = create_hex_serializer()
