from purescript.corefn.abs import NativeX

exports = {
    'unsafeCoerce': NativeX(lambda e: e, 1, [])
}
