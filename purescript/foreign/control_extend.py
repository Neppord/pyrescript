from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Array

exports = {
    'arrayExtend': NativeX(lambda f, xs: Array([
        f(xs[i:])
        for i, _ in enumerate(xs)
    ]), 2, []),
}