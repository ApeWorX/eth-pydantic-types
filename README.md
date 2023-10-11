# eth-pydantic-types

The types in this package are pydantic types for Ethereum inspired from [eth-typing](https://github.com/ethereum/eth-typing/blob/master/eth_typing/evm.py).

## Hash32

Hash32 is a good type to use for Ethereum transaction hashes.
`Hash` types serialize to bytes in the Pydantic core schema and `string` in the JSON schema with a binary format.
Use Hash32 like this:

```python
from pydantic import BaseModel

from eth_pydantic_types import Hash32

class Transaction(BaseModel):
    tx_hash: Hash32


# NOTE: I am able to pass an int-hash as the value and it will
#  get validated and type-coerced.
tx = Transaction(
    tx_hash=0x1031f0c9ac54dcb64b4f121a27957c14263c5cb49ed316d568e41e19c34d7b28
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
