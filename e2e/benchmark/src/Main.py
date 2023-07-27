from purescript.corefn.abs import NativeX
from purescript.corefn.literals import String, Effect


def _open(s):
    assert isinstance(s, String)
    file_name = s.value
    with file(file_name, "r") as f:
        out = f.read()
    return String(out)


exports = {
    'open': NativeX(lambda s: Effect(NativeX(_open, 1, [s])), 1, [])
}
