from corefn.abs import Native1
from corefn.literals import String, Int


def show_int_impl_(i, x):
    if not isinstance(x, Int):
        raise TypeError("expected Int got: " + x.__repr__())
    return String(str(x.value))


show_int_impl = Native1(show_int_impl_)