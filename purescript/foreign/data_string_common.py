from purescript.corefn.abs import NativeX
from purescript.corefn.literals import String


def _replace_all(i, replace, with_, in_):
    assert isinstance(replace, String)
    assert isinstance(with_, String)
    assert isinstance(in_, String)
    return String(in_.value.replace(replace.value, with_.value))


exports = {
    'replaceAll': NativeX(_replace_all, 3, [])
}
