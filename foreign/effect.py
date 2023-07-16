from corefn.abs import Foreign, AbsInterface
from corefn.literals import Effect, Native0


def bindE(interpreter, a):
    return Foreign("bindE", lambda atob: bindE_(interpreter, a, atob))


def bindE_(interpreter, a, atob):
    if isinstance(a, Effect):
        if isinstance(atob, AbsInterface):
            return Effect(Native0(lambda : atob.call_abs(interpreter, a.run_effect(interpreter)).run_effect(interpreter)))
        else:
            raise TypeError("expected Abs got: " + atob.__repr__())
    else:
        raise TypeError("expected Effect got: " + a.__repr__())