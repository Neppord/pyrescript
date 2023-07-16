from corefn.abs import Native1, BoundNative1
from corefn.literals import Unit, unit, Effect, Bound


def print_(i, s):
    print s.value
    return unit

def log_(i, x):
    return Effect(BoundNative1(print_, x))

log = Native1(log_)