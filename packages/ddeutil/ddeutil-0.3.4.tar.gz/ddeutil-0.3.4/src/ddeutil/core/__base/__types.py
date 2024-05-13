from __future__ import annotations

import sys
from numbers import Number
from typing import TypeVar, Union

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec


T = TypeVar("T")
P = ParamSpec("P")

Str = Union[str, bytes]
ZERO_DEPTH_BASES = (
    str,
    bytes,
    Number,
    range,
    bytearray,
)
