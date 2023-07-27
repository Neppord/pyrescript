from purescript.corefn.value import unit, String, NativeX
from purescript.foreign.effect import pureE


def print_(s):
    if not isinstance(s, String):
        raise TypeError("expected String got: " + s.__repr__())
    print s.value
    return unit


def log_(s):
    if not isinstance(s, String):
        raise TypeError("expected String got: " + s.__repr__())
    return pureE(NativeX(print_, 1, [s]))


log = NativeX(log_, 1, [])
