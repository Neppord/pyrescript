from purescript.corefn.abs import NativeX
from purescript.corefn.literals import String, Array


def concat_string(a, b):
    if not isinstance(a, String):
        raise TypeError("expected String got: " + a.__repr__())
    if not isinstance(b, String):
        raise TypeError("expected String got: " + b.__repr__())
    return String(a.value + b.value)


def concat_array(a, b):
    if not isinstance(a, Array):
        raise TypeError("expected Array got: " + a.__repr__())
    if not isinstance(b, Array):
        raise TypeError("expected Array got: " + b.__repr__())
    return Array(a.array + b.array)


exports = {
    'concatString': NativeX(concat_string, 2, []),
    'concatArray': NativeX(concat_array, 2, []),
}
