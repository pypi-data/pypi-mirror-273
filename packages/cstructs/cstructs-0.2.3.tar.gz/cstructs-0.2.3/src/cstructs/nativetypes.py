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
import typing
import struct

from cstructs.exc import InvalidTypeDef, ByteStringLengthMismatch


class NativeType:
    def __init__(
        self,
        name: str,
        size: int | None,
        python_type: type,
        struct_type: str,
        signed: bool,
        repeat_length: int = 1,
        encoding: str = "ascii",
        enforce_length: bool = False,
    ):
        self.name = name
        self.size = size
        self.python_type = python_type
        self.struct_type = struct_type
        self.signed = signed

        # repeat length is set in the __call__ method
        self.repeat_length = repeat_length

        # encoding is set in the __call__ method. it is used only by NativeTypes.char
        self.encoding = encoding
        self.enforce_length = enforce_length

    def __call__(
        self, repeat_length: int, encoding: str = "ascii", enforce_length: bool = False
    ):
        """
        Create a new instance of the native type with the specified repeat length, encoding, and enforce length option.

        Args:
            repeat_length (int): The number of times the native type repeats in the data.
            encoding (str, optional): The character encoding to use for string types. Defaults to "ascii".
            enforce_length (bool, optional): Whether to enforce the length of the repeated native type. Defaults to False.

        Returns:
            NativeType: A new instance of the native type with the specified repeat length, encoding, and enforce length option.

        Raises:
            InvalidTypeDef: If the repeat length is less than or equal to 0.
        """
        if repeat_length <= 0:
            raise InvalidTypeDef(
                f"repeat length must be greater than 0, got {repeat_length}"
            )

        return type(self)(
            self.name,
            self.size,
            self.python_type,
            self.struct_type,
            self.signed,
            repeat_length,
            encoding,
            enforce_length,
        )

    def __eq__(self, other):
        return (
            hasattr(other, "name")
            and self.name == other.name
            and hasattr(other, "size")
            and self.size == other.size
            and hasattr(other, "python_type")
            and self.python_type == other.python_type
            and hasattr(other, "struct_type")
            and self.struct_type == other.struct_type
            and hasattr(other, "signed")
            and self.signed == other.signed
        )

    def __repr__(self):
        return f"NativeType(typedef={self.name}, size={self.size}, repeat_length={self.repeat_length})"

    def __str__(self):
        return self.name

    def read(self, stream: typing.BinaryIO, byteorder: str):
        """
        Reads data from the given stream according to the specified byte order.

        Args:
            stream (typing.BinaryIO): The binary stream to read from.
            byteorder (str): The byte order to use for reading the data.

        Returns:
            The read data, based on the type and byte order.

        Raises:
            None.
        """
        if self.name == "char":
            return stream.read(self.repeat_length).decode(self.encoding)
        if self.name in ("pad", "bytestring"):
            return stream.read(self.repeat_length)

        format_str = f"{byteorder}{self.repeat_length}{self.struct_type}"

        return struct.unpack(format_str, stream.read(self.size * self.repeat_length))[0]

    def serialize(self, value, byteorder: str) -> bytes:
        """
        Serializes the given value into bytes according to the specified byte order.

        Args:
            value: The value to be serialized.
            byteorder: The byte order to be used for serialization.

        Returns:
            The serialized value as bytes.

        Raises:
            ByteStringLengthMismatch: If the length of the value does not match the repeat length
                and length enforcement is enabled.
        """
        if self.name == "char":
            if value is None:
                return b"\x00" * self.repeat_length

            if len(value) != self.repeat_length and self.enforce_length:
                raise ByteStringLengthMismatch(f"{len(value)} != {self.repeat_length}")

            return value.encode(self.encoding)
        if self.name == "bytestring":
            if value is None:
                return b"\x00" * self.repeat_length

            if len(value) != self.repeat_length and self.enforce_length:
                raise ByteStringLengthMismatch(f"{len(value)} != {self.repeat_length}")

            return value
        if self.name == "pad":
            if len(value) != self.repeat_length and self.enforce_length:
                raise ByteStringLengthMismatch(f"{len(value)} != {self.repeat_length}")

            return b"\x00" * self.repeat_length

        if value is None:
            if self.python_type is float:
                value = 0.0
            elif self.python_type is bool:
                value = False
            else:
                value = 0

        format_str = f"{byteorder}{self.repeat_length}{self.struct_type}"
        value &= (1 << (self.size * 8)) - 1

        if self.signed:
            bit_length = self.size * 8
            sign_bit = 1 << (bit_length - 1)

            if value & sign_bit:
                value -= 1 << bit_length

        return struct.pack(format_str, value)


class NativeTypes:
    """
    A class that defines native types used in cstructs.

    This class provides a set of predefined native types, such as integers, floats, characters, and booleans,
    along with their corresponding sizes, Python types, and format specifiers used in struct module.

    The class also includes special cases for bytestring and padding, which have variable sizes.

    Additionally, the class provides short and uppercase typedef names for convenience.

    Attributes:
        uint64 (NativeType): Unsigned 64-bit integer.
        uint32 (NativeType): Unsigned 32-bit integer.
        uint16 (NativeType): Unsigned 16-bit integer.
        uint8 (NativeType): Unsigned 8-bit integer.
        int64 (NativeType): Signed 64-bit integer.
        int32 (NativeType): Signed 32-bit integer.
        int16 (NativeType): Signed 16-bit integer.
        int8 (NativeType): Signed 8-bit integer.
        double (NativeType): Double precision floating-point number.
        float (NativeType): Single precision floating-point number.
        char (NativeType): String type.
        bool (NativeType): Boolean.
        bytestring (NativeType): Variable size byte string.
        pad (NativeType): Padding.
    """

    uint64 = NativeType("uint64", 8, int, "Q", False)
    uint32 = NativeType("uint32", 4, int, "I", False)
    uint16 = NativeType("uint16", 2, int, "H", False)
    uint8 = NativeType("uint8", 1, int, "B", False)
    int64 = NativeType("int64", 8, int, "q", True)
    int32 = NativeType("int32", 4, int, "i", True)
    int16 = NativeType("int16", 2, int, "h", True)
    int8 = NativeType("int8", 1, int, "b", True)
    double = NativeType("double", 8, float, "d", False)
    float = NativeType("float", 4, float, "f", False)
    char = NativeType("char", 1, str, "s", False)
    bool = NativeType("bool", 1, bool, "?", False)

    bytestring = NativeType("bytestring", None, bytes, "", False)
    pad = NativeType("pad", None, type(None), "", False)

    u64 = uint64
    u32 = uint32
    u16 = uint16
    u8 = uint8
    i64 = int64
    i32 = int32
    i16 = int16
    i8 = int8
    f64 = double
    f32 = float
    x = pad

    UINT64 = uint64
    UINT32 = uint32
    UINT16 = uint16
    UINT8 = uint8
    INT64 = int64
    INT32 = int32
    INT16 = int16
    INT8 = int8
    DOUBLE = double
    FLOAT = float
    CHAR = char
    BOOL = bool
    BYTESTRING = bytestring
    PAD = pad

    U64 = uint64
    U32 = uint32
    U16 = uint16
    U8 = uint8
    I64 = int64
    I32 = int32
    I16 = int16
    I8 = int8
    F64 = double
    F32 = float
    X = pad
