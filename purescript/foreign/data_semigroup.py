from purescript.corefn.literals import String


def concat_string(i, a, b):
    if not isinstance(a, String):
        raise TypeError("expected String got: " + a.__repr__())
    if not isinstance(b, String):
        raise TypeError("expected String got: " + b.__repr__())
    return String(a.value + b.value)
