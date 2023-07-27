from purescript.corefn.value import Int
from purescript.foreign import int_mod


def test_int_mod():
    assert int_mod(Int(0), Int(3)).value == 0
    assert int_mod(Int(3), Int(3)).value == 0
    assert int_mod(Int(6), Int(3)).value == 0

    assert int_mod(Int(0 + 1), Int(3)).value == 1
    assert int_mod(Int(3 + 1), Int(3)).value == 1
    assert int_mod(Int(6 + 1), Int(3)).value == 1

    assert int_mod(Int(0 + 2), Int(3)).value == 2
    assert int_mod(Int(3 + 2), Int(3)).value == 2
    assert int_mod(Int(6 + 2), Int(3)).value == 2

