from purescript.corefn.abs import NativeX

exports = {
    'arrayMap': NativeX(lambda i, f, a: [f(a_) for a_ in a], 2, []),
}
