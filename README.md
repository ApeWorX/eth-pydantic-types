# eth-pydantic-types

The types in this package are pydantic types for Ethereum inspired from [eth-typing](https://github.com/ethereum/eth-typing/blob/master/eth_typing/evm.py).

## HexStr

When your model involves a string serializes to a hex-str, `HexStr` is the type to use.
Examples of `HexStr` might be a hash.

Use `HexStr` in your models:

```python
from pydantic import BaseModel
from eth_pydantic_types import HexStr, HexStr32

class TransactionData(BaseModel):
    hash_any_size: HexStr
    sized_hash: HexStr32

data = TransactionData(hash_any_size="0x123", sized_hash="0x000123")
assert isinstance(data.nonce, str)
assert isinstance(data.gas, str)
```

## HexBytes

When your model involves bytes that serialize to a hex-str, `HexBytes` is the type to use.
Examples of `HexBytes` might be a hash.

Use `HexBytes` in your models:

```python
from pydantic import BaseModel
from eth_pydantic_types import HexBytes, HexBytes32

class TransactionData(BaseModel):
    hash_any_size: HexBytes
    sized_hash: HexBytes32

data = TransactionData(hash_any_size="0x123", sized_hash="0x000123")
assert isinstance(data.nonce, str)
assert isinstance(data.gas, str)
```

## HexInt

When your model involves an integer that serializes to a hex-str, `HexInt` is the type to use.
Examples of `HexInt` are transaction-type, nonce, and gas values.

Use `HexInt` in your models:

```python
from pydantic import BaseModel
from eth_pydantic_types import HexInt

class TransactionData(BaseModel):
    nonce: HexInt
    gas: HexInt

data = TransactionData(nonce="0x123", gas="0x000123")
assert isinstance(data.nonce, int)
assert isinstance(data.gas, int)
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
