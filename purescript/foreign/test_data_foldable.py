from purescript.corefn.abs import Foreign, Native3, Native2
from purescript.corefn.literals import Array, Int
from purescript.foreign import foldr_array, int_add, to_foreign
from purescript.foreign.data_foldable import foldr_array_


def test_foldr_array():
    assert foldr_array_(None, Native2(int_add), Int(0), Array([
        Int(1),
        Int(2),
        Int(3),
    ])).value == 6

    assert foldr_array_(None, to_foreign(lambda i, a, b: b), Int(0), Array([
        Int(1),
        Int(2),
        Int(3),
    ])).value == 0

def test_foldr_array_first():
    assert foldr_array_(None, Native2(first), Int(0), Array([
        Int(1),
        Int(2),
        Int(3),
    ])).value == 1

def first(i, a, b):
    return a