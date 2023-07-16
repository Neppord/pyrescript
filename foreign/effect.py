from corefn.abs import Foreign, AbsInterface, Native2, Native1
from corefn.literals import Effect, Bound




def bindE_(interpreter, a, atob):
    if isinstance(a, Effect):
        if isinstance(atob, AbsInterface):
            return Effect(Bound(lambda : atob.call_abs(interpreter, a.run_effect(interpreter)).run_effect(interpreter)))
        else:
            raise TypeError("expected Abs got: " + atob.__repr__())
    else:
        raise TypeError("expected Effect got: " + a.__repr__())


bindE = Native2(bindE_)
pureE = Native1(lambda i, x: Effect(x))
