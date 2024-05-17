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

from cstructs.datastruct.metadata import StructMeta, MetadataItem
from cstructs.exc import InvalidTypeDef
from cstructs import datastruct, DataStruct, NativeTypes

from typing import Annotated


def test_struct_meta_empty_class():
    """
    Test case to verify the behavior of metadata for an empty datastruct.

    This test case checks that the metadata for an empty datastruct is correctly
    created and accessible. It verifies that the `meta` attribute of the class
    is not None and is an instance of `StructMeta`. It also ensures that the
    metadata is iterable by iterating over it.
    """

    @datastruct
    class Test(metaclass=DataStruct):
        pass

    # meta should NOT be None and should be an instance of StructMeta
    assert isinstance(Test.meta, StructMeta)

    # ensure that the metadata is iterable
    for item in Test.meta:
        pass


def test_struct_meta_class_with_fields():
    """
    This test ensures that the metadata behaves like a sequence and implements dict-like behavior for metadata items.
    It also verifies that the metadata fields are accessible as instance fields and that each metadata item has a name, type, and size field.
    Additionally, it checks the correctness of the size of the bytestring field.
    """

    @datastruct
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint32
        b: Annotated[bytes, NativeTypes.bytestring(8)]

    # ensure that meta behaves like a sequence
    assert isinstance(Test.meta[0], MetadataItem)
    assert isinstance(Test.meta[1], MetadataItem)

    # ensure that the metadata also implements dict-like behavior
    assert isinstance(Test.meta["a"], MetadataItem)
    assert isinstance(Test.meta["b"], MetadataItem)

    # ensure that the metadata fields are also instance fields
    assert isinstance(Test.meta.a, MetadataItem)
    assert isinstance(Test.meta.b, MetadataItem)

    # ensure that each metadata item has a name, type, and size field
    assert Test.meta.a.name == "a"
    assert Test.meta.a.type == NativeTypes.uint32
    assert Test.meta.a.size == NativeTypes.uint32.size

    assert Test.meta.b.name == "b"
    assert Test.meta.b.type == NativeTypes.bytestring

    # ensure that the size of the bytestring is correct
    assert Test.meta.b.size == 8


def test_native_types():
    """
    Test case for native types in the datastruct.

    This test case verifies that the native types in the datastruct are correctly defined
    and have the expected metadata fields.

    It checks the following:
    - The metadata fields are also instance fields.
    - Each metadata item has a name, type, and size field.
    - The type field can be either the long typedef or the short typedef.
    - The native types have a field that represents the typedef as a Python primitive.

    Raises:
        AssertionError: If any of the assertions fail.
    """

    @datastruct
    class Test(metaclass=DataStruct):
        a: NativeTypes.uint32
        b: NativeTypes.u32
        c: Annotated[int, NativeTypes.uint16(4)]
        d: NativeTypes.u16
        e: NativeTypes.uint8
        f: NativeTypes.u8
        g: NativeTypes.int32
        h: NativeTypes.i32
        i: NativeTypes.int16
        j: NativeTypes.i16
        k: NativeTypes.int8
        l: NativeTypes.i8
        m: NativeTypes.float
        n: NativeTypes.double
        o: NativeTypes.bool
        p: NativeTypes.char
        q: Annotated[bytes, NativeTypes.bytestring(10)]
        r: NativeTypes.uint64
        s: NativeTypes.u64
        t: NativeTypes.int64
        u: NativeTypes.i64

    # ensure that the metadata fields are also instance fields
    assert isinstance(Test.meta.a, MetadataItem)
    assert isinstance(Test.meta.b, MetadataItem)

    # ensure that each metadata item has a name, type, and size field
    assert Test.meta.a.name == "a"

    # ensure that the type field can be either the long typedef or the short typedef
    assert Test.meta.a.type in (NativeTypes.uint32, NativeTypes.u32)
    assert Test.meta.a.size == NativeTypes.uint32.size

    # ensure that the native types have a field that represents this typedef as a
    # python primitive
    assert NativeTypes.uint32.python_type == int

    # edit: redundant test
    # ensure that an error is raised if the repeat length is less than or equal to 0
    # with pytest.raises(InvalidTypeDef):
    #     NativeTypes.uint32(0)
