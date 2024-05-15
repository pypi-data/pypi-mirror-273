# Module stacchip.chipper

## Classes

### Chipper

```python3
class Chipper(
    platform: str,
    item_id: str,
    bucket: str = '',
    mountpath: str = '',
    indexer: stacchip.indexer.ChipIndexer = None,
    asset_blacklist: List[str] = ['scl', 'qa_pixel']
)
```

Chipper class

#### Methods

    
#### chip

```python3
def chip(
    self,
    x: int,
    y: int
) -> dict
```

Chip pixel array for the x and y index numbers

    
#### get_pixels_for_asset

```python3
def get_pixels_for_asset(
    self,
    key: str,
    x: int,
    y: int
) -> Union[numpy._typing._array_like._SupportsArray[numpy.dtype[Any]], numpy._typing._nested_sequence._NestedSequence[numpy._typing._array_like._SupportsArray[numpy.dtype[Any]]], bool, int, float, complex, str, bytes, numpy._typing._nested_sequence._NestedSequence[Union[bool, int, float, complex, str, bytes]]]
```

Extract chip pixel values for one asset

    
#### load_indexer_local

```python3
def load_indexer_local(
    self,
    mountpath: pathlib.Path,
    platform: str,
    item_id: str
) -> stacchip.indexer.ChipIndexer
```

Load stacchip index table from local file

    
#### load_indexer_s3

```python3
def load_indexer_s3(
    self,
    bucket: str,
    platform: str,
    item_id: str
) -> stacchip.indexer.ChipIndexer
```

Load stacchip index table from a remote location