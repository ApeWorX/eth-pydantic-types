# eth-pydantic-types

The types in this package are pydantic types for Ethereum inspired from [eth-typing](https://github.com/ethereum/eth-typing/blob/master/eth_typing/evm.py).

## Hash

`Bytes{n}` and `String{n}` are good types to use when your hex values are sized.
Both types serialize to `string` in the JSON schema.
Use `Bytes` types when you want types to serialize to bytes in the Pydantic core schema and `String` types when you want to serialize to `str` in the core Pydantic schema.

```python
from pydantic import BaseModel

from eth_pydantic_types import Bytes32, String20

# When serializing to JSON, both types are hex strings.
class Transaction(BaseModel):
    tx_hash: Bytes32  # Will be bytes
    address: String20  # Will be str


# NOTE: I am able to pass an int-hash as the value and it will
#  get validated and type-coerced.
tx = Transaction(
    tx_hash=0x1031f0c9ac54dcb64b4f121a27957c14263c5cb49ed316d568e41e19c34d7b28,
    address=0x1031f0c9ac54dcb64b4f121a27957c14263c5cb4,
)
```

## HexBytes

A thin-wrapper around an already thin-wrapper `hexbytes.HexBytes`.
The difference here is that this HexBytes properly serializes.
Use HexBytes any place where you would actually use `hexbytes.HexBytes`.
`HexBytes` serializes to bytes in the Pydantic core schema and `string` in the JSON schema with a binary format.

```python
from pydantic import BaseModel
from eth_pydantic_types import HexBytes

class MyStorage(BaseModel):
    cid: HexBytes

# NOTE: We are able to pass a hex-str for a HexBytes value.
storage = MyStorage(cid="0x123")
```

## Address

Use the Address class for working with checksummed-addresses.
Addresses get validated and checksummed in model construction.
Addresses serialize to `str` in the Pydantic core schema and `string` in the JSON schema with a binary format.

```python
from pydantic import BaseModel
from eth_pydantic_types import Address

class Account(BaseModel):
    address: Address

# NOTE: The address ends up checksummed
#   ("0x0837207e343277CBd6c114a45EC0e9Ec56a1AD84")
account = Account(address="0x837207e343277cbd6c114a45ec0e9ec56a1ad84")
```

## HexStr

Use hex str when you only care about un-sized hex strings.
The `HexStr` type serializes to `str` in the Pydantic core schema and a `string` in the JSON schema with a binary format.

```python
from eth_pydantic_types import HexStr
from pydantic import BaseModel

class Tx(BaseModel):
    data: HexStr

tx = Tx(data="0x0123")
```

## Bip122Uri

Use BIP-122 URIs in your models by annotating with the `Bip122Uri` type.
This type serializes to a `str` in the Pydantic core schema as well as a `string` in the JSON schema, however the individual hashes are validated.

```python
from eth_pydantic_types import Bip122Uri
from pydantic import BaseModel

class Message(BaseModel):
    path: Bip122Uri

message = Message(
    path=(
        "blockchain://d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3"
        "/block/752820c0ad7abc1200f9ad42c4adc6fbb4bd44b5bed4667990e64565102c1ba6"
    )
)
```
