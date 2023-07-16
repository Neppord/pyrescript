from corefn.abs import Native1
from corefn.literals import String, Int


def show_int_impl_(i, x):
    if isinstance(x, Int):
        return String(str(x.value))
    else:
        raise TypeError("expected Int got: " + x.__repre__())

show_int_impl = Native1(show_int_impl_)