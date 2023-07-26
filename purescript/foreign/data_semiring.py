from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Int, Float


def int_add(i, a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    return Int(a.value + b.value)


def int_mul(i, a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    return Int(a.value * b.value)


exports = {
    'intAdd': NativeX(int_add, 2, []),
    'intMul': NativeX(int_mul, 2, []),
    'numAdd': NativeX(lambda i, a, b: Float(a.value + b.value), 2, []),
    'numMul': NativeX(lambda i, a, b: Float(a.value * b.value), 2, []),
}
