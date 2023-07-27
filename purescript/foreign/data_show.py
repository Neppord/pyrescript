from purescript.corefn.abs import NativeX
from purescript.corefn.value import String, Int


def show_int_impl_(x):
    if not isinstance(x, Int):
        raise TypeError("expected Int got: " + x.__repr__())
    return String(str(x.value))


exports = {
    'showIntImpl': NativeX(show_int_impl_, 1, []),
    'showStringImpl': NativeX(lambda v: String(str(v)), 1, []),
    'showCharImpl': NativeX(lambda v: String(str(v)), 1, []),
    'showNumberImpl': NativeX(lambda v: String(str(v)), 1, []),
}
