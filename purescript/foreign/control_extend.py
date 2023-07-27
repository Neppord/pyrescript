from purescript.corefn.value import Array, NativeX

exports = {
    'arrayExtend': NativeX(lambda f, xs: Array([
        f(xs[i:])
        for i, _ in enumerate(xs)
    ]), 2, []),
}
