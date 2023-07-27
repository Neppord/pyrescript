from purescript.corefn.abs import NativeX
from purescript.corefn.value import Boolean, Int


def eq_int_impl(a, b):
    if not isinstance(a, Int):
        raise TypeError("expected Int got: " + a.__repr__())
    if not isinstance(b, Int):
        raise TypeError("expected Int got: " + b.__repr__())
    return Boolean(a.value == b.value)


exports = {
    'eqIntImpl': NativeX(eq_int_impl, 2, []),
    'eqStringImpl': NativeX(lambda a, b: Boolean(a == b), 2, []),
    'eqNumberImpl': NativeX(lambda a, b: Boolean(a == b), 2, []),
    'eqCharImpl': NativeX(lambda a, b: Boolean(a == b), 2, []),
    'eqBooleanImpl': NativeX(lambda a, b: Boolean(a == b), 2, []),
    'eqArrayImpl': NativeX(lambda a, b: Boolean(a == b), 2, []),
}
