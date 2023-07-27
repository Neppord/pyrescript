from purescript.corefn.value import String, NativeX


def _replace_all(replace, with_, in_):
    assert isinstance(replace, String)
    assert isinstance(with_, String)
    assert isinstance(in_, String)
    return String(in_.value.replace(replace.value, with_.value))


exports = {
    'replaceAll': NativeX(_replace_all, 3, [])
}
