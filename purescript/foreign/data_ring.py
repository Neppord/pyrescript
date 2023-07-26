from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Int, Float


def _intSub(i, a, b):
    assert isinstance(a, Int)
    assert isinstance(b, Int)
    return Int(a.value - b.value)

exports = {
    'intSub': NativeX(_intSub, 2, []),
    'numSub': NativeX(lambda i, a, b: Float(a.value - b.value), 2, []),
}