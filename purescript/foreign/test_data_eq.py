from purescript.corefn.literals import Int
from purescript.foreign import eq_int_impl


def test_eq_int_impl():
    assert not eq_int_impl(None, Int(1), Int(0)).value
    assert not eq_int_impl(None, Int(0), Int(1)).value
    assert eq_int_impl(None, Int(1), Int(1)).value
