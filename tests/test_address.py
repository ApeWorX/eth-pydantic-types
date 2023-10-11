import pytest
from pydantic import BaseModel, ValidationError

from eth_pydantic_types.address import Address
from eth_pydantic_types.hex import HexBytes

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
    prop = actual["properties"]["address"]
    assert prop["maxLength"] == 42
    assert prop["minLength"] == 42
    assert prop["type"] == "string"
    assert prop["pattern"] == "^0x[a-fA-F0-9]{40}$"
    assert prop["examples"] == [
        "0x0000000000000000000000000000000000000000",
        "0x02c84e944F97F4A4f60221e6fb5d5DbAE49c7aaB",
        "0xa5a13f62ce1113838e0d9b4559b8caf5f76463c0",
        "0x1e59ce931B4CFea3fe4B875411e280e173cB7A9C",
    ]


def test_model_dump():
    model = Model(address=ADDRESS)
    actual = model.model_dump()
    expected = {"address": CHECKSUM_ADDRESS}
    assert actual == expected
