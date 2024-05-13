from __future__ import annotations

import importlib
import operator
import sys
import typing
from collections.abc import Callable, Collection
from math import ceil

from .cache import (
    clear_cache,
    memoize,
    memoized_property,
)
from .checker import (
    can_int,
    is_int,
)
from .convert import (
    must_bool,
    must_list,
    str2any,
    str2args,
    str2bool,
    str2dict,
    str2int_float,
    str2list,
)
from .hash import (
    checksum,
    freeze,
    freeze_args,
    hash_all,
    hash_pwd,
    hash_str,
    random_str,
    same_pwd,
    tokenize,
)
from .merge import (
    merge_dict,
    merge_dict_value,
    merge_dict_values,
    merge_list,
    merge_values,
    zip_equal,
)
from .sorting import (
    ordered,
    sort_priority,
)
from .splitter import (
    isplit,
    must_rsplit,
    must_split,
)

T = typing.TypeVar("T")

concat: typing.Callable[[typing.Any], str] = "".join


def operate(x):
    return getattr(operator, x)


def is_generic(t: type):
    """Return True if type in the generic alias type."""
    return hasattr(t, "__origin__")


def not_generic(check: typing.Any, instance):
    if instance is typing.NoReturn:
        return check is None
    elif instance is typing.Any:
        return True
    return isinstance(check, instance)


def isinstance_check(check: typing.Any, instance) -> bool:
    """Return True if check data is instance.

    Examples:
        >>> import typing as t
        ... assert isinstance_check(['s', ], t.List[str])
        ... assert isinstance_check(('s', 't', ), t.Tuple[str, ...])
        ... assert not isinstance_check(('s', 't', ), t.Tuple[str])
        ... assert isinstance_check({'s': 1, 'd': 'r'}, t.Dict[
        ...     str, t.Union[int, str]]
        ... )
        ... assert isinstance_check('s', t.Optional[str])
        ... assert isinstance_check(1, t.Optional[t.Union[str, int]])
        ... assert not isinstance_check('s', t.List[str])
        ... assert isinstance_check([1, '2'], t.List[t.Union[str, int]])
        ... assert not isinstance_check('s', t.NoReturn)
        ... assert isinstance_check(None, t.NoReturn)
        ... assert isinstance_check('A', t.Any)
        ... assert isinstance_check([1, [1, 2, 3]], t.List[
        ...     t.Union[t.List[int], int]
        ... ])
    """
    if not is_generic(instance):
        return not_generic(check, instance)

    origin = typing.get_origin(instance)
    if origin == typing.Union:
        return any(
            isinstance_check(check, typ) for typ in typing.get_args(instance)
        )

    if not issubclass(check.__class__, origin):
        return False

    if origin == dict:
        _dict = typing.get_args(instance)
        return all(
            (isinstance_check(k, _dict[0]) and isinstance_check(v, _dict[1]))
            for k, v in check.items()
        )
    elif origin in {
        tuple,
        list,
    }:
        _dict = typing.get_args(instance)
        if Ellipsis in _dict or (origin is not tuple):
            return all(isinstance_check(i, _dict[0]) for i in iter(check))
        try:
            return all(
                isinstance_check(i[0], i[1]) for i in zip_equal(check, _dict)
            )
        except ValueError:
            return False
    elif origin is Callable:
        return callable(check)
    raise NotImplementedError("It can not check typing instance of this pair.")


def cached_import(module_path, class_name):
    """Cached import package"""
    modules = sys.modules
    if (
        module_path not in modules
        or getattr(modules[module_path], "__spec__", None) is not None
        and getattr(modules[module_path].__spec__, "_initializing", False)
    ):
        importlib.import_module(module_path)
    return getattr(modules[module_path], class_name)


def import_string(dotted_path: str):
    """Import a dotted module path and return the attribute/class designated by
    the last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(
            f"{dotted_path} doesn't look like a module path"
        ) from err

    try:
        return cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(
            f'Module "{module_path}" does not define a "{class_name}" '
            f"attribute/class"
        ) from err


def round_up(number: float, decimals):
    """
    Examples:
        >>> round_up(1.00406, 2)
        1.01
        >>> round_up(1.00001, 1)
        1.1
    """
    assert isinstance(number, float)
    assert isinstance(decimals, int)
    assert decimals >= 0
    if decimals == 0:
        return ceil(number)
    factor = 10**decimals
    return ceil(number * factor) / factor


def remove_pad(value: str) -> str:
    """Remove zero padding of string
    Examples:
        >>> remove_pad('000')
        '0'
        >>> remove_pad('0123')
        '123'
        >>> remove_pad('0000123')
        '123'
    """
    return _last_char if (_last_char := value[-1]) == "0" else value.lstrip("0")


def onlyone(
    check: list[T],
    value: list[T],
    *,
    default: bool = True,
) -> T | None:
    """Get only one element from check list that exists in match list.

    Examples:
        >>> onlyone(['a', 'b'], ['a', 'b', 'c'])
        'a'
        >>> onlyone(['a', 'b'], ['c', 'e', 'f'])
        'c'
        >>> onlyone(['a', 'b'], ['c', 'e', 'f'], default=False)

    """
    if len(exist := set(check).intersection(set(value))) == 1:
        return list(exist)[0]
    return next(
        (_ for _ in value if _ in check),
        (value[0] if default else None),
    )


def hasdot(search: str, content: dict[typing.Any, typing.Any]) -> bool:
    """Return True value if dot searching exists in content data.

    Examples:
        >>> hasdot('data.value', {'data': {'value': 2}})
        True
        >>> hasdot('data.value.key', {'data': {'value': 2}})
        False
        >>> hasdot('item.value.key', {'data': {'value': 2}})
        False
    """
    _search, _else = must_split(search, ".", maxsplit=1)
    if _search in content and isinstance(content, dict):
        if not _else:
            return True
        elif isinstance((result := content[_search]), dict):
            return hasdot(_else, result)
    return False


def getdot(
    search: str,
    content: dict[typing.Any, typing.Any],
    *args,
    **kwargs,
) -> typing.Any:
    """Return the value if dot searching exists in content data.

    Examples:
        >>> getdot('data.value', {'data': {'value': 1}})
        1
        >>> getdot('data', {'data': 'test'})
        'test'
        >>> getdot('data.value', {'data': 'test'})
        Traceback (most recent call last):
        ...
        ValueError: 'value' does not exists in test
        >>> getdot('data.value', {'data': {'key': 1}}, None)

        >>> getdot(
        ...     'data.value.getter',
        ...     {'data': {'value': {'getter': 'success', 'put': 'fail'}}},
        ... )
        'success'
        >>> getdot('foo.bar', {"foo": {"baz": 1}}, ignore=True)

        >>> getdot('foo.bar', {"foo": {"baz": 1}}, 2, 3)
        2
        >>> getdot('foo.bar', {"foo": {"baz": 1}}, 2, 3, ignore=True)
        2
    """
    _ignore: bool = kwargs.get("ignore", False)
    _search, _else = must_split(search, ".", maxsplit=1)
    if _search in content and isinstance(content, dict):
        if not _else:
            return content[_search]
        if isinstance((result := content[_search]), dict):
            return getdot(_else, result, *args, **kwargs)
        if _ignore:
            return None
        raise ValueError(f"{_else!r} does not exists in {result}")
    if args:
        return args[0]
    elif _ignore:
        return None
    raise ValueError(f"{_search} does not exists in {content}")


def setdot(search: str, content: dict, value: typing.Any, **kwargs) -> dict:
    """
    Examples:
        >>> setdot('data.value', {'data': {'value': 1}}, 2)
        {'data': {'value': 2}}
        >>> setdot('data.value.key', {'data': {'value': 1}}, 2, ignore=True)
        {'data': {'value': 1}}
    """
    _ignore: bool = kwargs.get("ignore", False)
    _search, _else = must_split(search, ".", maxsplit=1)
    if _search in content and isinstance(content, dict):
        if not _else:
            content[_search] = value
            return content
        if isinstance((result := content[_search]), dict):
            content[_search] = setdot(_else, result, value, **kwargs)
            return content
        if _ignore:
            return content
        raise ValueError(f"{_else!r} does not exists in {result}")
    if _ignore:
        return content
    raise ValueError(f"{_search} does not exists in {content}")


def filter_dict(
    value: T,
    included: Collection | None = None,
    excluded: Collection | None = None,
) -> T:
    """
    Examples:
        >>> filter_dict({"foo": "bar"}, included={}, excluded={"foo"})
        {}
        >>> filter_dict(
        ...     {"foo": 1, "bar": 2, "baz": 3},
        ...     included=("foo", )
        ... )
        {'foo': 1}
        >>> filter_dict(
        ...     {"foo": 1, "bar": 2, "baz": 3},
        ...     included=("foo", "bar", ),
        ...     excluded=("bar", )
        ... )
        {'foo': 1}
    """
    _exc: Collection = excluded or ()
    return dict(
        filter(
            lambda i: i[0]
            in (v for v in (included or value.keys()) if v not in _exc),
            value.items(),
        )
    )
