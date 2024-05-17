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

from cstructs import datastruct, NativeTypes, DataStruct
from cstructs.exc import ByteStringLengthMismatch
from typing import Annotated


def test_write_basic():
    """
    Test case for basic write functionality of a datastruct.
    """

    @datastruct(byteorder="big")
    class Test(metaclass=DataStruct):
        a: NativeTypes.u8
        b: NativeTypes.i8

        def on_write(self, data: bytes):
            assert data.hex() == bytes.fromhex("01FF").hex()

    # datastructs must be usable even without initial data
    test = Test.init_empty()

    test.a = 1

    # ensure values are appropiately scaled to their typedef's width
    test.b = 0xFFFF
    hexstr = test.serialize().hex()

    assert hexstr == bytes.fromhex("01FF").hex()

    test.b = 0xFF
    hexstr = test.serialize().hex()

    assert hexstr == bytes.fromhex("01FF").hex()


def test_write_complex():
    """
    Test case for serializing a complex datastruct.

    Raises:
        ByteStringLengthMismatch: If the length of the `d` field is not equal to 6.

    Returns:
        None
    """

    @datastruct(byteorder="big")
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint32
        b: NativeTypes.i8
        c: NativeTypes.char
        d: Annotated[str, NativeTypes.char(6, enforce_length=True)]
        e: Annotated[bytes, NativeTypes.bytestring(8)]

    test = Test.init_empty()

    test.a = 1

    # ensure all None values get properly encoded to 0(null)
    # fmt: off
    assert test.serialize() == bytes.fromhex(
        "00 00 00 01"
        "00"
        "00"
        "00 00 00 00 00 00"
        "00 00 00 00 00 00 00 00"
    )
    # fmt: on

    test.a = 0xFFFFFFFF
    test.b = 0xFF
    test.c = "!"
    test.d = "Anthy!"
    test.e = b"\x00\x01\x02\x03\x04\x05\x06\x07"

    # fmt: off
    assert test.serialize() == bytes.fromhex(
        "FF FF FF FF"
        "FF"
        "21"
        "41 6E 74 68 79 21"
        "00 01 02 03 04 05 06 07"
    )
    # fmt: on

    # ensure that mismatching lengths are reported
    with pytest.raises(ByteStringLengthMismatch):
        test.d = "Anthy!!!"

        test.serialize()
