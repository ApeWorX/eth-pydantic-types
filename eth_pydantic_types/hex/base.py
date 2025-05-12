from typing import ClassVar

schema_pattern = "^0x([0-9a-f][0-9a-f])*$"
schema_examples = (
    "0x",  # empty bytes
    "0xd4",
    "0xd4e5",
    "0xd4e56740",
    "0xd4e56740f876aef8",
    "0xd4e56740f876aef8c010b86a40d5f567",
    "0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3",
)


class BaseHex:
    size: ClassVar[int] = 0
    schema_pattern: ClassVar[str] = schema_pattern
    schema_examples: ClassVar[tuple[str, ...]] = schema_examples

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(
            format="binary", pattern=cls.schema_pattern, examples=list(cls.schema_examples)
        )
        return json_schema
