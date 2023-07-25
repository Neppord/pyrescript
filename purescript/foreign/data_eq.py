from purescript.corefn.literals import Boolean, Int


def eq_int_impl(i, a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    return Boolean(a.value == b.value)
