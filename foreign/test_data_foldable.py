from corefn.abs import Foreign
from corefn.literals import ArrayLiteral, IntLiteral
from foreign import foldr_array, int_add, to_foreign
from foreign.data_foldable import foldr_array_


def test_foldr_array():
    assert foldr_array_(None, to_foreign(int_add), IntLiteral(0), ArrayLiteral([
        IntLiteral(1),
        IntLiteral(2),
        IntLiteral(3),
    ])).value == 6

    assert foldr_array_(None, to_foreign(lambda a, b: b), IntLiteral(0), ArrayLiteral([
        IntLiteral(1),
        IntLiteral(2),
        IntLiteral(3),
    ])).value == 0

    assert foldr_array_(None, Foreign("", lambda a: Foreign("", lambda b: a)), IntLiteral(0), ArrayLiteral([
        IntLiteral(1),
        IntLiteral(2),
        IntLiteral(3),
    ])).value == 1
