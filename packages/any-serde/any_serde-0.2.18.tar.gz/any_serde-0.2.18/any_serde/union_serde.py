import types
from typing import (
    Any,
    List,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)
from any_serde.common import (
    InvalidSerializationException,
    InvalidDeserializationException,
    JSON,
    resolve_newtypes,
    truncate_str,
)


T_Any = TypeVar("T_Any")


def _get_union_args(type_: Type[T_Any]) -> Sequence[Type[Any]]:
    type_origin_nullable = get_origin(type_)

    assert type_origin_nullable is not None, f"Calling union serde on non-union type: {type_}"

    type_origin = resolve_newtypes(type_origin_nullable)
    type_args = [resolve_newtypes(type_arg) for type_arg in get_args(type_)]

    assert type_origin in (Union, types.UnionType), f"Calling union serde on non-union type: {type_}"

    seen: Set[Type[Any]] = set()
    deduped_type_args: List[Type[Any]] = []
    for type_arg in type_args:
        if type_arg in seen:
            continue
        deduped_type_args.append(type_arg)
        seen.add(type_arg)

    return deduped_type_args


def from_data(
    type_: Type[T_Any],
    data: JSON,
) -> T_Any:
    type_args = _get_union_args(type_)

    from any_serde import serde

    for union_arg in type_args:
        try:
            return serde.from_data(union_arg, data)
        except InvalidDeserializationException:
            pass

    raise InvalidDeserializationException("Could not deserialize to any union option.")


def to_data(
    type_: Type[T_Any],
    item: T_Any,
) -> JSON:
    type_args = _get_union_args(type_)

    from any_serde import serde

    for union_arg in type_args:
        try:
            return serde.to_data(union_arg, item)
        except InvalidSerializationException:
            pass

    raise InvalidSerializationException(f"No union option for {type_} matches {truncate_str(str(item))}")
