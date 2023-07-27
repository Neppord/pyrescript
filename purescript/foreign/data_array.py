from purescript.corefn.literals import Array, Int


def range_impl(start, end):
    if not isinstance(start, Int):
        raise TypeError("expected Int got: " + start.__repr__())
    if not isinstance(end, Int):
        raise TypeError("expected Int got: " + end.__repr__())
    return Array([Int(x) for x in range(start.value, end.value + 1)])
