from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Boolean

exports = {
    'boolConj': NativeX(lambda i, a, b: Boolean(a.value and b.value), 2, []),
    'boolDisj': NativeX(lambda i, a, b: Boolean(a.value or b.value), 2, []),
    'boolNot': NativeX(lambda i, b: Boolean(not b.value), 1, []),
}