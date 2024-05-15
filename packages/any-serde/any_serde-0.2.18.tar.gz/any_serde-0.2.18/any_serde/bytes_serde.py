from typing import Type
import base64
import io

from any_serde.common import (
    JSON,
    InvalidDeserializationException,
)


def from_data(type_: Type[bytes], data: JSON) -> bytes:
    if not isinstance(data, str):
        raise InvalidDeserializationException(f"Cannot deserialize {type(data)} to bytes. Must be str!")

    assert type_ is bytes

    encoded_bytes = data.encode("utf-8")
    encoded_io = io.BytesIO()
    encoded_io.write(encoded_bytes)
    encoded_io.seek(0)
    decoded_io = io.BytesIO()

    base64.decode(input=encoded_io, output=decoded_io)
    decoded_io.seek(0)
    return decoded_io.read()


def to_data(type_: Type[bytes], item: bytes) -> str:
    assert isinstance(item, bytes)
    assert type_ is bytes

    decoded_io = io.BytesIO()
    decoded_io.write(item)
    decoded_io.seek(0)
    encoded_io = io.BytesIO()
    base64.encode(input=decoded_io, output=encoded_io)
    encoded_io.seek(0)
    encoded_bytes = encoded_io.read()
    return str(encoded_bytes, "utf-8")
