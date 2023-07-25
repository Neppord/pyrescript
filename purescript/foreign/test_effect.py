from purescript.corefn.abs import Foreign
from purescript.corefn.literals import Effect, Int
from purescript.foreign.effect import bindE_


def test_bind_e_():
    assert bindE_(
        None,
        Effect(Int(1)),
        Foreign("inc", lambda i: Effect(Int(i.value + 1)))
    ).run_effect(None).value == 2
