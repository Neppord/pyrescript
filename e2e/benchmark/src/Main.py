from purescript.corefn.abs import NativeX
from purescript.corefn.value import String
from purescript.foreign.effect import pureE


def _open(s):
    assert isinstance(s, String)
    file_name = s.value
    with file(file_name, "r") as f:
        out = f.read()
    return String(out)


exports = {
    'open': NativeX(lambda s: pureE(NativeX(_open, 1, [s])), 1, [])
}
