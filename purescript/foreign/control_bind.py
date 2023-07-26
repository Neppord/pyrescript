from purescript.corefn.abs import NativeX

exports = {
    'arrayBind': NativeX(lambda i, arr, f: [f(a) for a in arr], 2, [])
}