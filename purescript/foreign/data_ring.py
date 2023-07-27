from purescript.corefn.abs import NativeX
from purescript.corefn.value import Int, Float


def _intSub(a, b):
    assert isinstance(a, Int)
    assert isinstance(b, Int)
    return Int(a.value - b.value)

exports = {
    'intSub': NativeX(_intSub, 2, []),
    'numSub': NativeX(lambda a, b: Float(a.value - b.value), 2, []),
}