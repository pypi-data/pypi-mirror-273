from collections.abc import Mapping
import enum
from typing import Annotated

from numpy.typing import ArrayLike


class CompressionLevel(enum.Enum):
    Fast: CompressionLevel

    Default: CompressionLevel

    High: CompressionLevel

class Filter(enum.Enum):
    Adaptive: Filter

    None: Filter

    Sub: Filter

    Up: Filter

    Average: Filter

    Paeth: Filter

class Strategy(enum.Enum):
    Adaptive: Strategy

    Default: Strategy

    Filtered: Strategy

    Huffman: Strategy

    Rle: Strategy

    Fixed: Strategy

def encode_png(image: Annotated[ArrayLike, dict(dtype='uint8', order='C', device='cpu')], writable: object, filter: Filter = Filter.Adaptive, strategy: Strategy = Strategy.Rle, compression_level: CompressionLevel = CompressionLevel.Default, info: Mapping[str, str] = {}) -> None:
    """Encode PNG to writable object."""

def encode_u16_png(image: Annotated[ArrayLike, dict(dtype='uint16', order='C', device='cpu')], writable: object, filter: Filter = Filter.Adaptive, strategy: Strategy = Strategy.Rle, compression_level: CompressionLevel = CompressionLevel.Default, info: Mapping[str, str] = {}) -> None:
    """Encode 16bit PNG to writable object."""
