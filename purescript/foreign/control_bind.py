from purescript.corefn.value import NativeX

exports = {
    'arrayBind': NativeX(lambda arr, f: [f(a) for a in arr], 2, [])
}