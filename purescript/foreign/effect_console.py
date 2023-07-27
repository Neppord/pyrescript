from purescript.corefn.abs import NativeX
from purescript.corefn.literals import unit, Effect, String


def print_(s):
    if not isinstance(s, String):
        raise TypeError("expected String got: " + s.__repr__())
    print s.value
    return unit


def log_(s):
    if not isinstance(s, String):
        raise TypeError("expected String got: " + s.__repr__())
    return Effect(NativeX(print_, 1, [s]))


log = NativeX(log_, 1, [])