from purescript.corefn.value import NativeX

exports = {
    'unsafeCoerce': NativeX(lambda e: e, 1, [])
}
