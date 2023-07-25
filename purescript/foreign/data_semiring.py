from purescript.corefn.literals import Int


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
