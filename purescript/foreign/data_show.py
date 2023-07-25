from purescript.corefn.abs import NativeX
from purescript.corefn.literals import String, Int


def show_int_impl_(i, x):
    if not isinstance(x, Int):
        raise TypeError("expected Int got: " + x.__repr__())
    return String(str(x.value))


show_int_impl = NativeX(show_int_impl_, 1, [])