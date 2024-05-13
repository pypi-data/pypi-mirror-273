from __future__ import annotations

from typing import Any

TrueStr: tuple[str, ...] = (
    "yes",
    "y",
    "true",
    "t",
    "1",
    "1.0",
    "o",
)

FalseStr: tuple[str, ...] = (
    "no",
    "n",
    "false",
    "f",
    "0",
    "0.0",
    "x",
)


def is_int(value: Any) -> bool:
    """Check value that is integer.

    Examples:
        >>> is_int('')
        False
        >>> is_int('0.0')
        False
        >>> is_int('-3'), int('-3')
        (True, -3)
        >>> is_int('-123.4')
        False
        >>> is_int('543')
        True
        >>> is_int('0'), int('0')
        (True, 0)
        >>> is_int('-')
        False
        >>> is_int('+13'), int('+13')
        (True, 13)
    """
    if isinstance(value, int):
        return True
    elif not value:
        return False

    # Note:
    #   For Python string type, it has builtin checking methods like:
    #   ``str.isdigit()``, ``str.isdecimal()``, or ``str.isnumeric()``.
    return (
        _value[1:].isdecimal()
        if (_value := str(value))[0] in {"-", "+"}
        else _value.isdecimal()
    )


def can_int(value: Any) -> bool:
    """Check value that able to integer (but some value does not use int() to
    convert it such as 0.0 or 3.0).

    Examples:
        >>> can_int('0.0')
        True
        >>> can_int('-1.0')
        True
        >>> can_int('1.1')
        False
        >>> can_int('s')
        False
        >>> can_int('1')
        True
        >>> can_int(1.0)
        True
    """
    try:
        return float(str(value)).is_integer()
    except (TypeError, ValueError):
        return False
