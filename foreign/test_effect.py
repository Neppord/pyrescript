from corefn.abs import Foreign
from corefn.literals import Effect, Int, Lazy2, Bound1
from foreign.effect import bindE_


def test_bind_e_():
    assert bindE_(
        None,
        Effect(Int(1)),
        Foreign("inc", lambda i: Effect(Int(i.value + 1)))
    ).run_effect(None).value == 2
