from purescript.corefn.abs import NativeX

exports = {
    'arrayBind': NativeX(lambda arr, f: [f(a) for a in arr], 2, [])
}