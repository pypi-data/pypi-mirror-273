from enum import Enum
from typing import Type, TypeVar, Any
from any_serde import json_serde
from any_serde.common import InvalidDeserializationException, JSON, InvalidSerializationException

T_Enum = TypeVar("T_Enum", bound=Enum)


ATTR_SERIALIZE_BY_VALUE = "__serialize_by_value__"


def is_enum_type(typ: Any) -> bool:
    return isinstance(typ, type) and issubclass(typ, Enum)


def from_data(type_: Type[T_Enum], data: JSON) -> T_Enum:
    assert is_enum_type(type_)

    if getattr(type_, ATTR_SERIALIZE_BY_VALUE, False):
        try:
            return type_(data)
        except ValueError:
            raise InvalidDeserializationException(f"[{type_}] Value {data} is not a valid {type_}!")

    if not isinstance(data, str):
        raise InvalidDeserializationException(f"Enums serialize to strings. Got {type(data)} instead!")

    split_items = data.split(".")

    if len(split_items) != 2:
        raise InvalidDeserializationException(f"Serialized enums are EnumType.ENUM_VALUE. Got {data} instead!")

    enum_type_str, enum_value_str = split_items

    enum_value = type_[enum_value_str]

    if not data == str(enum_value):
        raise InvalidDeserializationException(f"Wrong Enum type? Expected {type_}, got {enum_type_str}!")

    return enum_value


def to_data(type_: Type[T_Enum], enum_value: Enum) -> JSON:
    assert is_enum_type(type_), f"Trying enum.to_data on type {type_}"
    assert isinstance(enum_value, Enum), f"Trying enum.to_data on value type {type(enum_value)}"

    try:
        mapped_value = type_[enum_value.name]
    except KeyError:
        raise InvalidSerializationException(f"Could not convert {enum_value} ({type(enum_value)} to {type_})")

    if getattr(type_, ATTR_SERIALIZE_BY_VALUE, False):
        try:
            return json_serde.validate_json(mapped_value.value)
        except ValueError:
            raise InvalidSerializationException(f"[{type_}] {mapped_value} has invalid value!")

    return str(mapped_value)


def serialize_by_value(type_: Type[T_Enum]) -> Type[T_Enum]:
    assert is_enum_type(type_)
    setattr(type_, ATTR_SERIALIZE_BY_VALUE, True)
    return type_
