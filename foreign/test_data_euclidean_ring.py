from corefn.literals import IntLiteral
from foreign import int_mod


def test_int_mod():
    assert int_mod(IntLiteral(0), IntLiteral(3)).value == 0
    assert int_mod(IntLiteral(3), IntLiteral(3)).value == 0
    assert int_mod(IntLiteral(6), IntLiteral(3)).value == 0

    assert int_mod(IntLiteral(0 + 1), IntLiteral(3)).value == 1
    assert int_mod(IntLiteral(3 + 1), IntLiteral(3)).value == 1
    assert int_mod(IntLiteral(6 + 1), IntLiteral(3)).value == 1

    assert int_mod(IntLiteral(0 + 2), IntLiteral(3)).value == 2
    assert int_mod(IntLiteral(3 + 2), IntLiteral(3)).value == 2
    assert int_mod(IntLiteral(6 + 2), IntLiteral(3)).value == 2

