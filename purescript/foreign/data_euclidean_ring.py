from purescript.corefn.literals import Int


def int_mod(i, a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    abs_b = abs(b.value)
    return Int(((a.value % abs_b) + abs_b) % abs_b)


def int_degree(i, x):
    raise NotImplementedError()


def int_div(i, a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    return Int(a.value // b.value)
