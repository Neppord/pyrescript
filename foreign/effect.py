from corefn.abs import Foreign, AbsInterface, Native2, Native1, BoundNative2, BoundBoundNative2
from corefn.literals import Effect, Bound


def bindE__(i, a, atob):
    return atob.call_abs(i, a.run_effect(i)).run_effect(i)


def bindE_(interpreter, a, atob):
    if not isinstance(a, Effect):
        raise TypeError("expected Effect got: " + a.__repr__())
    if not isinstance(atob, AbsInterface):
        raise TypeError("expected Abs got: " + atob.__repr__())
    return Effect(BoundBoundNative2(bindE__, a, atob))


bindE = Native2(bindE_)
pureE = Native1(lambda i, x: Effect(x))
