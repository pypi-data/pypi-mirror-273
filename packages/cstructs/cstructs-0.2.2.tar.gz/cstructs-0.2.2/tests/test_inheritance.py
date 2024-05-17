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
import io

from cstructs import datastruct, DataStruct, NativeTypes


def test_inheritance():
    @datastruct(byteorder="big")
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint32
        b: NativeTypes.uint32

    @datastruct(byteorder="big")
    class Test2(Test, metaclass=DataStruct):
        c: NativeTypes.u8

        def on_read(self):
            assert self.a == 1
            assert self.b == 2
            assert self.c == 3

    stream = io.BytesIO()
    stream.write(b"00 00 00 01")
    stream.write(b"00 00 00 02")
    stream.write(b"03")

    stream.seek(0)

    Test.read(stream)
