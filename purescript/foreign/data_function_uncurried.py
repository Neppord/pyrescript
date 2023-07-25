from purescript.corefn.abs import NativeX

exports = {
    'mkFn4': NativeX(lambda i, fn: fn, 1, []),
    'runFn4': NativeX(lambda i, fn: fn, 1, []),
    'mkFn2': NativeX(lambda i, fn: fn, 1, []),
    'runFn2': NativeX(lambda i, fn: fn, 1, []),
}