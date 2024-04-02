from pydantic_core.core_schema import plain_serializer_function_ser_schema


def serialize_hex(value: bytes):
    hex_value = value.hex()
    return hex_value if hex_value.startswith("0x") else f"0x{hex_value}"


hex_serializer = plain_serializer_function_ser_schema(function=serialize_hex)
