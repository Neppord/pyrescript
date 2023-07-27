from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Array

exports = {
    'arrayApply': NativeX(lambda fs, xs: Array([f(x) for x in xs.array for f in fs]), 2, [])
}
