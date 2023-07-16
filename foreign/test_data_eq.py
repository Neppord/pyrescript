from corefn.literals import IntLiteral
from foreign import eq_int_impl


def test_eq_int_impl():
    assert not eq_int_impl(IntLiteral(1), IntLiteral(0)).value
    assert not eq_int_impl(IntLiteral(0), IntLiteral(1)).value
    assert eq_int_impl(IntLiteral(1), IntLiteral(1)).value
