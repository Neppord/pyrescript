from purescript.corefn.abs import Native2, Native3
from purescript.corefn.literals import String


def _replace_all(i, replace, with_, in_):
    assert isinstance(replace, String)
    assert isinstance(with_, String)
    assert isinstance(in_, String)
    return String(in_.value.replace(replace.value, with_.value))

exports = {
    'replaceAll': Native3(_replace_all)
}