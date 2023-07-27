from purescript.corefn.value import Array, NativeX

exports = {
    'arrayApply': NativeX(lambda fs, xs: Array([f(x) for x in xs.array for f in fs]), 2, [])
}
