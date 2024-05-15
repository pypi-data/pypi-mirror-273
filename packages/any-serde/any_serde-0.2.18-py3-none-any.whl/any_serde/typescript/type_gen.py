from __future__ import annotations
from enum import Enum
import json

import types
import dataclasses
from typing import Any, List, Literal, Optional, Type, Union, get_args, get_origin

from any_serde import dataclass_serde
import any_serde.enum
from any_serde.common import resolve_newtypes
from any_serde.typescript.typescript_utils import (
    TYPESCRIPT_MODULE_DIR,
    load_template,
)

LiteralValueType = Union[None, int, bool, str, bytes, Enum]


DESERIALIZATION_ERROR_NAME = "any_serde.DeserializationError"
RAISE_DESERIALIZATION_ERROR = f'const e = Error(); e.name = "{DESERIALIZATION_ERROR_NAME}"; throw e'
SERIALIZATION_ERROR_NAME = "any_serde.SerializationError"
RAISE_SERIALIZATION_ERROR = f'const e = Error(); e.name = "{SERIALIZATION_ERROR_NAME}"; throw e'


class InvalidTypescriptTypeException(Exception):
    """Failed to convert Python type to Typescript type."""


@dataclasses.dataclass
class TypescriptTypedef:
    type_: Type[Any]
    filepath: list[str]
    code: str
    dependencies: list[TypescriptTypedef]

    value_type_name: str
    value_type_requires_import: bool

    data_type_name: str
    data_type_requires_import: bool

    to_data_name: str
    from_data_name: str


string_typescript_template = load_template(TYPESCRIPT_MODULE_DIR / "string_typedef.ts.jinja2")
string_typescript_code = string_typescript_template.render(
    RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
)
STRING_TYPESCRIPT_TYPEDEF = TypescriptTypedef(
    type_=str,
    filepath=["builtin_typedefs.ts"],
    code=string_typescript_code,
    dependencies=[],
    value_type_name="string",
    value_type_requires_import=False,
    data_type_name="string",
    data_type_requires_import=False,
    to_data_name="string__to_data",
    from_data_name="string__from_data",
)


int_typescript_template = load_template(TYPESCRIPT_MODULE_DIR / "int_typedef.ts.jinja2")
int_typescript_code = int_typescript_template.render(
    RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
    RAISE_SERIALIZATION_ERROR=RAISE_SERIALIZATION_ERROR,
)
INT_TYPESCRIPT_TYPEDEF = TypescriptTypedef(
    type_=int,
    filepath=["builtin_typedefs.ts"],
    code=int_typescript_code,
    dependencies=[],
    value_type_name="int",
    value_type_requires_import=True,
    data_type_name="int__DATA",
    data_type_requires_import=True,
    to_data_name="int__to_data",
    from_data_name="int__from_data",
)


float_typescript_template = load_template(TYPESCRIPT_MODULE_DIR / "float_typedef.ts.jinja2")
float_typescript_code = float_typescript_template.render(
    RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
)
FLOAT_TYPESCRIPT_TYPEDEF = TypescriptTypedef(
    type_=float,
    filepath=["builtin_typedefs.ts"],
    code=float_typescript_code,
    dependencies=[],
    value_type_name="number",
    value_type_requires_import=False,
    data_type_name="number",
    data_type_requires_import=False,
    to_data_name="float__to_data",
    from_data_name="float__from_data",
)


bool_typescript_template = load_template(TYPESCRIPT_MODULE_DIR / "bool_typedef.ts.jinja2")
bool_typescript_code = bool_typescript_template.render(
    RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
)
BOOL_TYPESCRIPT_TYPEDEF = TypescriptTypedef(
    type_=bool,
    filepath=["builtin_typedefs.ts"],
    code=bool_typescript_code,
    dependencies=[],
    value_type_name="boolean",
    value_type_requires_import=False,
    data_type_name="boolean",
    data_type_requires_import=False,
    to_data_name="bool__to_data",
    from_data_name="bool__from_data",
)

none_typescript_template = load_template(TYPESCRIPT_MODULE_DIR / "none_typedef.ts.jinja2")
none_typescript_code = none_typescript_template.render(
    RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
)
NONE_TYPESCRIPT_TYPEDEF = TypescriptTypedef(
    type_=None,  # type: ignore[arg-type]
    filepath=["builtin_typedefs.ts"],
    code=none_typescript_code,
    dependencies=[],
    value_type_name="null",
    value_type_requires_import=False,
    data_type_name="null",
    data_type_requires_import=False,
    to_data_name="none__to_data",
    from_data_name="none__from_data",
)

nonetype_typescript_template = load_template(TYPESCRIPT_MODULE_DIR / "nonetype_typedef.ts.jinja2")
nonetype_typescript_code = nonetype_typescript_template.render(
    RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
)
NONETYPE_TYPESCRIPT_TYPEDEF = TypescriptTypedef(
    type_=type(None),
    filepath=["builtin_typedefs.ts"],
    code=nonetype_typescript_code,
    dependencies=[],
    value_type_name="null",
    value_type_requires_import=False,
    data_type_name="null",
    data_type_requires_import=False,
    to_data_name="nonetype__to_data",
    from_data_name="nonetype__from_data",
)


class TypescriptTypedefStore:
    def __init__(self) -> None:
        self.typedefs: list[TypescriptTypedef] = [
            STRING_TYPESCRIPT_TYPEDEF,
            INT_TYPESCRIPT_TYPEDEF,
            FLOAT_TYPESCRIPT_TYPEDEF,
            BOOL_TYPESCRIPT_TYPEDEF,
            NONE_TYPESCRIPT_TYPEDEF,
            NONETYPE_TYPESCRIPT_TYPEDEF,
        ]

    def _find_by_type(self, type_: Type[Any]) -> Optional[TypescriptTypedef]:
        """Finds the typedef for a python type, if already registered."""
        for typedef in self.typedefs:
            if typedef.type_ == type_:
                return typedef

        return None

    def _create_literal_typedef(
        self,
        type_: Type[Any],
        literal_values: List[LiteralValueType],
        name: str,
        filepath: list[str],
    ) -> TypescriptTypedef:
        def get_value_str(literal_value: LiteralValueType) -> str:
            if isinstance(literal_value, bytes):
                raise NotImplementedError("Cannot use bytes literals in TypeScript yet!")

            from any_serde import to_data

            literal_data = to_data(type_, literal_value)  # type: ignore[arg-type]
            literal_str = json.dumps(literal_data)
            return literal_str

        literal_value_strs = list(map(get_value_str, literal_values))
        if len(set(literal_value_strs)) < len(literal_value_strs):
            raise ValueError("Multiple literal values map to the same typescript value!")

        value_type_name = name
        data_type_name = f"{name}__DATA"
        to_data_name = f"{name}__to_data"
        from_data_name = f"{name}__from_data"
        literal_code_template = load_template(TYPESCRIPT_MODULE_DIR / "literal_typedef.ts.jinja2")
        literal_code = literal_code_template.render(
            value_type_name=value_type_name,
            data_type_name=data_type_name,
            to_data_name=to_data_name,
            from_data_name=from_data_name,
            RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
            literal_value_strs=literal_value_strs,
        )
        return TypescriptTypedef(
            type_=type_,
            filepath=filepath,
            code=literal_code,
            dependencies=[],
            value_type_name=value_type_name,
            value_type_requires_import=True,
            data_type_name=data_type_name,
            data_type_requires_import=True,
            to_data_name=to_data_name,
            from_data_name=from_data_name,
        )

    def _create_typescript_typedef(
        self,
        type_: Type[Any],
        name: str,
        filepath: list[str],
    ) -> TypescriptTypedef:
        """Creates a new typedef."""
        if any_serde.enum.is_enum_type(type_):
            return self._create_literal_typedef(
                type_=type_,
                literal_values=list(type_),  # type: ignore[call-overload]
                name=name,
                filepath=filepath,
            )

        if dataclass_serde.is_dataclass_type(type_):
            value_type_name = name
            data_type_name = f"{name}__DATA"
            to_data_name = f"{name}__to_data"
            from_data_name = f"{name}__from_data"
            field_types = dataclass_serde._get_type_hints(type_)  # type: ignore[arg-type]
            field_typedefs = [
                (
                    f.name,
                    self._find_or_create_by_type(
                        type_=field_types[f.name],
                        name=f"{name}__{f.name}",
                        filepath=filepath,
                    ),
                )
                for f in dataclasses.fields(type_)
            ]
            dataclass_code_template = load_template(TYPESCRIPT_MODULE_DIR / "dataclass_typedef.ts.jinja2")
            dataclass_code = dataclass_code_template.render(
                value_type_name=value_type_name,
                data_type_name=data_type_name,
                to_data_name=to_data_name,
                from_data_name=from_data_name,
                field_typedefs=field_typedefs,
                RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
            )
            return TypescriptTypedef(
                type_=type_,
                filepath=filepath,
                code=dataclass_code,
                dependencies=[field_typedef for _field_name, field_typedef in field_typedefs],
                value_type_name=value_type_name,
                value_type_requires_import=True,
                data_type_name=data_type_name,
                data_type_requires_import=True,
                to_data_name=to_data_name,
                from_data_name=from_data_name,
            )

        type_origin_nullable = get_origin(type_)
        if type_origin_nullable is None:
            raise InvalidTypescriptTypeException(f"Unsupported type: {type_}")

        type_origin = resolve_newtypes(type_origin_nullable)
        type_args = [resolve_newtypes(type_arg) for type_arg in get_args(type_)]

        if type_origin in (Union, types.UnionType):
            value_type_name = name
            data_type_name = f"{name}__DATA"
            to_data_name = f"{name}__to_data"
            from_data_name = f"{name}__from_data"

            union_typedefs = [
                self._find_or_create_by_type(
                    type_=union_arg_type,
                    name=f"{name}__{union_arg_idx}",
                    filepath=filepath,
                )
                for union_arg_idx, union_arg_type in enumerate(type_args)
            ]
            union_code_template = load_template(TYPESCRIPT_MODULE_DIR / "union_typedef.ts.jinja2")
            union_code = union_code_template.render(
                value_type_name=value_type_name,
                data_type_name=data_type_name,
                to_data_name=to_data_name,
                from_data_name=from_data_name,
                union_typedefs=union_typedefs,
                DESERIALIZATION_ERROR_NAME=DESERIALIZATION_ERROR_NAME,
                RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
                enumerate=enumerate,
            )
            return TypescriptTypedef(
                type_=type_,
                filepath=filepath,
                code=union_code,
                dependencies=union_typedefs,
                value_type_name=value_type_name,
                value_type_requires_import=True,
                data_type_name=data_type_name,
                data_type_requires_import=True,
                to_data_name=to_data_name,
                from_data_name=from_data_name,
            )

        if type_origin in (list, set):
            value_type_name = name
            data_type_name = f"{name}__DATA"
            to_data_name = f"{name}__to_data"
            from_data_name = f"{name}__from_data"

            (list_item_type,) = type_args
            item_typedef = self._find_or_create_by_type(
                type_=list_item_type,
                name=name + "_item",
                filepath=filepath,
            )
            list_code_template = load_template(TYPESCRIPT_MODULE_DIR / "list_typedef.ts.jinja2")
            list_code = list_code_template.render(
                value_type_name=value_type_name,
                data_type_name=data_type_name,
                to_data_name=to_data_name,
                from_data_name=from_data_name,
                item_typedef=item_typedef,
                RAISE_DESERIALIZATION_ERROR=RAISE_DESERIALIZATION_ERROR,
            )
            return TypescriptTypedef(
                type_=type_,
                filepath=filepath,
                code=list_code,
                dependencies=[item_typedef],
                value_type_name=value_type_name,
                value_type_requires_import=True,
                data_type_name=data_type_name,
                data_type_requires_import=True,
                to_data_name=to_data_name,
                from_data_name=from_data_name,
            )

        if type_origin is dict:
            raise NotImplementedError("TODO: handle dicts")

        if type_origin is tuple:
            raise NotImplementedError("TODO: handle tuples")

        if type_origin is Literal:
            return self._create_literal_typedef(
                type_=type_,
                literal_values=type_args,  # type: ignore[arg-type]
                name=name,
                filepath=filepath,
            )

        raise NotImplementedError(f"Unrecognized type: {type_}")

    def _find_or_create_by_type(
        self,
        type_: Type[Any],
        name: str,
        filepath: list[str],
    ) -> TypescriptTypedef:
        found_type = self._find_by_type(type_)
        if found_type is not None:
            return found_type

        return self.get_typescript_typedef(
            type_=type_,
            name=name,
            filepath=filepath,
        )

    def get_typescript_typedef(
        self,
        type_: Type[Any],
        name: str,
        filepath: list[str],
    ) -> TypescriptTypedef:
        """Create and get a typedef for the given type and name and write location."""
        typedef = self._create_typescript_typedef(
            type_=type_,
            name=name,
            filepath=filepath,
        )
        self.typedefs.append(typedef)
        return typedef

    def get_single_file_code(self) -> str:
        code = ""
        first = True
        for typedef in self.typedefs:
            if not first:
                code += "\n"
            first = False
            code += typedef.code
            code += "\n"

        return code
