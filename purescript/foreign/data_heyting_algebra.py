from purescript.corefn.value import Boolean, NativeX

exports = {
    'boolConj': NativeX(lambda a, b: Boolean(a.value and b.value), 2, []),
    'boolDisj': NativeX(lambda a, b: Boolean(a.value or b.value), 2, []),
    'boolNot': NativeX(lambda b: Boolean(not b.value), 1, []),
}