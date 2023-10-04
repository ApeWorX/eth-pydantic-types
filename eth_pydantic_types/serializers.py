from pydantic_core.core_schema import plain_serializer_function_ser_schema

hex_serializer = plain_serializer_function_ser_schema(function=lambda x: x.hex())
