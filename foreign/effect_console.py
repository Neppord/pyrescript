from corefn.abs import Native1, BoundNative1
from corefn.literals import unit, Effect, String


def print_(i, s):
    if not isinstance(s, String): raise TypeError("expected String got: " + s.__repr__())
    print s.value
    return unit


def log_(i, s):
    if not isinstance(s, String): raise TypeError("expected String got: " + s.__repr__())
    return Effect(BoundNative1(print_, s))


log = Native1(log_)
