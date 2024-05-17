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
import struct
import typing

from cstructs.datastruct import DataStructMeta
from cstructs.nativetypes import NativeTypes


def read_struct(struct_cls: DataStructMeta, stream: typing.BinaryIO) -> DataStructMeta:
    for item in struct_cls.meta:
        if item.type is NativeTypes.PAD:
            stream.read(item.size)

            continue

        if item.type.size is None:
            item.value = item.type.read(stream)
        else:
            item.value = item.type.read(stream, item.size)
