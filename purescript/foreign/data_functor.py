from purescript.corefn.abs import NativeX

exports = {
    'arrayMap': NativeX(lambda f, a: [f(a_) for a_ in a], 2, []),
}
