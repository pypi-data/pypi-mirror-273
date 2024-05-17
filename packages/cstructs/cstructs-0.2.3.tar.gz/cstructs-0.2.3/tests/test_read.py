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
import pytest
import io

from cstructs import datastruct, NativeTypes, DataStruct
from typing import Annotated


def test_read_basic():
    """
    Test case for reading basic data from a stream.

    This test case defines a datastruct using the `datastruct` decorator and the `DataStruct` metaclass.
    It reads two unsigned 8 bit values from a byte stream and asserts that the values are correctly read and assigned to the data structure.

    The expected values are:
    - `a`: 1
    - `b`: 2
    """

    @datastruct
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint8
        b: NativeTypes.uint8

        def on_read(
            self,
        ):
            assert self.a == 1
            assert self.b == 2

    stream = io.BytesIO(bytes.fromhex("01 02"))
    test = Test.read(stream)

    assert test.a == 1
    assert test.b == 2


def test_read_complex():
    """
    Test case for reading complex data using a datastruct.

    This test case verifies that the datastruct can correctly read complex data from a stream.

    The Test class is defined using the `datastruct` decorator and the `DataStruct` metaclass.
    It has several fields of different types, including integers, bytes, and strings.

    The test case creates a `BytesIO` stream and writes a sequence of bytes representing the complex data.
    It then seeks back to the beginning of the stream and uses the `Test.read` method to read the data.

    Finally, the test case asserts that the read data matches the expected values.

    Raises:
        AssertionError: If any of the assertions fail.

    """

    @datastruct(byteorder="big")
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint16
        b: NativeTypes.uint32
        c: NativeTypes.i32
        d: NativeTypes.uint64
        e: Annotated[bytes, NativeTypes.bytestring(4)]
        f: Annotated[str, NativeTypes.char(12)]
        g: Annotated[str, NativeTypes.char(1, encoding="latin1")]

    stream = io.BytesIO()

    stream.write(bytes.fromhex("0001"))
    stream.write(bytes.fromhex("00000002"))
    stream.write(bytes.fromhex("fffffffd"))
    stream.write(bytes.fromhex("0000000000000004"))
    stream.write(bytes.fromhex("01020304"))
    stream.write(b"Hello World!")
    stream.write(bytes.fromhex("BF"))

    stream.seek(0)

    test = Test.read(stream)

    assert test.a == 1
    assert test.b == 2
    assert test.c == -3
    assert test.d == 4
    assert test.e == b"\x01\x02\x03\x04"
    assert test.f == "Hello World!"
    assert test.g == "¿"
