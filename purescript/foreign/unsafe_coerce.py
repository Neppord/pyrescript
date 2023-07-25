from purescript.corefn.abs import NativeX

exports = {
    'unsafeCoerce': NativeX(lambda i, e: e, 1, [])
}
