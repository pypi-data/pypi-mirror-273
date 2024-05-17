# --------------------------------------------------------------------------------------
#  Copyright(C) 2023 yntha                                                             -
#                                                                                      -
#  This program is free software: you can redistribute it and/or modify it under       -
#  the terms of the GNU General Public License as published by the Free Software       -
#  Foundation, either version 3 of the License, or (at your option) any later          -
#  version.                                                                            -
#                                                                                      -
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY     -
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A     -
#  PARTICULAR PURPOSE. See the GNU General Public License for more details.            -
#                                                                                      -
#  You should have received a copy of the GNU General Public License along with        -
#  this program. If not, see <http://www.gnu.org/licenses/>.                           -
# --------------------------------------------------------------------------------------
import dataclasses
import io
import typing

from cstructs.exc import InvalidByteOrder, InvalidTypeDef
from cstructs.datastruct.metadata import StructMeta, MetadataItem
from cstructs.nativetypes import NativeType


_byteorder_map = {"native": "@", "little": "<", "network": "!", "big": ">"}


class DataStruct(type):
    """
    Metaclass for defining datastructs.

    This metaclass provides functionality for reading data from a binary stream and constructing an instance of the datastruct.
    It also provides a method for initializing an empty instance of said datastruct.

    Attributes:
        on_read (typing.Callable[[], None] | None): A callback function to be called after reading data from a binary stream.
        on_write (typing.Callable[[type, bytearray], None] | None): A callback function to be called after all data has been serialized it takes in one parameter, a bytearray, containing the serialized data..
        meta (StructMeta | None): The metadata that describes the structure of the data.
        byteorder (str | None): Specifies the byte order of the data.
        size (int | None): Specifies the size of the data in bytes.
        serialize (typing.Callable[[], bytearray] | None): A function for serializing the data. It is added later to the class, as an instance method of the datastruct.

    Methods:
        read(cls, stream: typing.BinaryIO) -> Any: Reads data from a binary stream and constructs an instance of the class.
        init_empty(cls) -> Any: Initializes an empty instance of the class.
    """

    def __new__(cls, *args, **kwargs):
        cls.on_read: typing.Callable[[], None] | None = None
        cls.on_write: typing.Callable[[bytearray], None] | None = None
        cls.meta: StructMeta | None = None
        cls.byteorder: str | None = None
        cls.size: int | None = None
        cls.serialize: typing.Callable[[], bytearray] | None = None

        return type.__new__(cls, *args, **kwargs)

    def read(cls, stream: typing.BinaryIO) -> typing.Any:
        """
        Reads data from a binary stream and constructs an instance of the class.

        Args:
            stream (typing.BinaryIO): The binary stream to read from.

        Returns:
            The constructed instance of the class.

        Raises:
            TypeError: If the stream is not a binary stream.
        """
        if not isinstance(stream, io.IOBase):
            raise TypeError("Expected a binary stream")

        for item in cls.meta:
            item.value = item.type.read(stream, _byteorder_map[cls.byteorder])

        self = cls(**{p.name: p.value for p in cls.meta})

        if cls.on_read is not None:
            cls.on_read(self)

        return self

    def init_empty(cls) -> typing.Any:
        """
        Initializes an empty instance of the class.

        Returns:
            An empty instance of the class.
        """
        return cls(**{p.name: None for p in cls.meta})


def datastruct(
    cls: typing.Optional[type] = None, /, *, byteorder: str = "native"
) -> typing.Callable[..., type]:
    """
    Decorator function for creating dataclasses capable of parsing and serialization.

    Args:
        cls (type, optional): The class to decorate. If not provided, the decorator is returned.
        byteorder (str, optional): The byte order to use for serialization. Defaults to "native".

    Returns:
        Callable[..., type]: The decorated class or the decorator itself.

    Raises:
        InvalidByteOrder: If the provided byte order is invalid.
        InvalidTypeDef: If the type definition for a field is invalid.

    Example usage:
        @datastruct
        class MyStruct:
            field1: int
            field2: str
    """
    if byteorder not in _byteorder_map:
        raise InvalidByteOrder(f"Invalid byteorder: {byteorder}")

    def decorator(struct_cls):
        dataclass_cls = dataclasses.dataclass(struct_cls)

        dataclass_cls.byteorder = byteorder
        dataclass_cls.meta = StructMeta()

        for field in dataclasses.fields(dataclass_cls):
            is_annotated = typing.get_origin(field.type) == typing.Annotated

            if not isinstance(field.type, NativeType) and not is_annotated:
                raise InvalidTypeDef(
                    f"Invalid type definition for {field.name}: {field.type}"
                )

            if is_annotated:
                _, typedef = typing.get_args(field.type)
                is_special = typedef.size is None

                item_name = field.name
                item_size = typedef.size if not is_special else typedef.repeat_length
                item_typedef = typedef
            else:
                item_name = field.name
                item_size = field.type.size
                item_typedef = field.type

            dataclass_cls.meta.add_item(
                MetadataItem(item_name, item_typedef, item_size)
            )

            def serializer(self) -> bytearray:
                buf = bytearray()

                for item in self.meta:
                    buf.extend(
                        item.type.serialize(
                            getattr(self, item.name), _byteorder_map[self.byteorder]
                        )
                    )

                if self.__class__.on_write is not None:  # noqa
                    self.on_write(buf)

                return buf

            setattr(dataclass_cls, "serialize", serializer)

        dataclass_cls.size = sum([item.size for item in dataclass_cls.meta])
        dataclass_cls.__qualname__ = f"cstructs.datastruct.{dataclass_cls.__name__}"

        return dataclass_cls

    if cls is None:
        return decorator

    return decorator(cls)
