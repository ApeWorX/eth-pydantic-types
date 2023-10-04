import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.address import Address
from eth_pydantic_types.hexbytes import HexBytes

# NOTE: This address purposely is the wrong length (missing left zero),
#   not checksummed, and not 0x prefixed.
ADDRESS = "837207e343277cbd6c114a45ec0e9ec56a1ad84"
CHECKSUM_ADDRESS = "0x0837207e343277CBd6c114a45EC0e9Ec56a1AD84"


class Model(BaseModel):
    address: Address


@pytest.fixture
def checksum_address():
    return CHECKSUM_ADDRESS


@pytest.mark.parametrize(
    "address",
    (
        CHECKSUM_ADDRESS,
        ADDRESS,
        f"0x{ADDRESS}",
        f"0x0{ADDRESS}",
        int(ADDRESS, 16),
        HexBytes(ADDRESS),
    ),
)
def test_address(address, checksum_address):
    actual = Model(address=address)
    assert actual.address == checksum_address


@pytest.mark.parametrize("address", ("foo", -35, "0x" + ("F" * 100)))
def test_invalid_address(address):
    with pytest.raises(ValidationError):
        Model(address=address)


def test_schema():
    actual = Model.model_json_schema()
    for name, prop in actual["properties"].items():
        assert prop["maxLength"] == 42
        assert prop["minLength"] == 42
        assert prop["type"] == "string"
        assert prop["pattern"] == "^0x[a-fA-F0-9]{40}$"


def test_model_dump():
    model = Model(address=ADDRESS)
    actual = model.model_dump()
    expected = {"address": CHECKSUM_ADDRESS}
    assert actual == expected
