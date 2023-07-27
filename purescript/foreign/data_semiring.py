from purescript.corefn.value import Int, Float, NativeX


def int_add(a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    return Int(a.value + b.value)


def int_mul(a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    return Int(a.value * b.value)


exports = {
    'intAdd': NativeX(int_add, 2, []),
    'intMul': NativeX(int_mul, 2, []),
    'numAdd': NativeX(lambda a, b: Float(a.value + b.value), 2, []),
    'numMul': NativeX(lambda a, b: Float(a.value * b.value), 2, []),
}
