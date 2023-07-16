from corefn.abs import Foreign
from corefn.literals import Array, Int
from foreign import foldr_array, int_add, to_foreign
from foreign.data_foldable import foldr_array_


def test_foldr_array():
    assert foldr_array_(None, to_foreign(int_add), Int(0), Array([
        Int(1),
        Int(2),
        Int(3),
    ])).value == 6

    assert foldr_array_(None, to_foreign(lambda a, b: b), Int(0), Array([
        Int(1),
        Int(2),
        Int(3),
    ])).value == 0

    assert foldr_array_(None, Foreign("", lambda a: Foreign("", lambda b: a)), Int(0), Array([
        Int(1),
        Int(2),
        Int(3),
    ])).value == 1
