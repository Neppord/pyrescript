from purescript.corefn.value import NativeX


def _unsafe_partial(value):
    return value


exports = {
    '_unsafePartial': NativeX(_unsafe_partial, 1, [])
}
