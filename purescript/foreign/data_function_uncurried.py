from purescript.corefn.value import NativeX

exports = {
    'mkFn4': NativeX(lambda fn: fn, 1, []),
    'mkFn2': NativeX(lambda fn: fn, 1, []),
    'runFn4': NativeX(lambda fn: fn, 1, []),
    'runFn2': NativeX(lambda fn: fn, 1, []),
}
