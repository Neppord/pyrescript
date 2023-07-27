from purescript.corefn.abs import NativeX
from purescript.corefn.value import Int, Float


def int_mod(a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    abs_b = abs(b.value)
    return Int(((a.value % abs_b) + abs_b) % abs_b)


def int_degree(x):
    raise NotImplementedError()


def int_div(a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    return Int(a.value // b.value)


exports = {
    'intDegree': NativeX(int_degree, 1, []),
    'intDiv': NativeX(int_div, 2, []),
    'intMod': NativeX(int_mod, 2, []),
    'numDiv': NativeX(lambda a, b: Float(a.value / b.value), 2, []),
}
