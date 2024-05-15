from typing import Any, Union, TypeVar, Type, Dict, List


JSON_PRIMITIVE_TYPES = [
    str,
    int,
    float,
    bool,
    None,
    type(None),
]
JSONPrimitive = Union[
    str,
    int,
    float,
    bool,
    None,
]
JSON = Union[
    JSONPrimitive,
    Dict[str, "JSON"],
    List["JSON"],
]


T_Any = TypeVar("T_Any")


def resolve_newtypes(typ: Type[T_Any]) -> Type[T_Any]:
    # https://github.com/python/mypy/issues/3325
    while hasattr(typ, "__supertype__"):
        typ = getattr(typ, "__supertype__")
    return typ


class InvalidDeserializationException(Exception):
    """Indicates that the given data is not valid for the target type given."""


class InvalidSerializationException(Exception):
    """Indicates that the given variable could not be serialized."""


class Undefined:
    """A value that does not get serialized. Should only be used as dataclass values."""

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Undefined)


class UndefinedValueException(Exception):
    """Indicates that an Undefined was (correctly) serialized."""


def truncate_str(s: str, max_length: int = 80) -> str:
    if len(s) <= max_length:
        return s

    return s[:48] + "..." + s[-49:]
