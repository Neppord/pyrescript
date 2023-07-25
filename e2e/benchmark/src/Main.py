from purescript.corefn.abs import Native1, BoundNative1
from purescript.corefn.literals import String, Effect


def _open(i, s):
    assert isinstance(s, String)
    file_name = s.value
    with file(file_name, "r") as f:
        out = f.read()
    return String(out)


exports = {
    'open': Native1(lambda i, s: Effect(BoundNative1(_open, s)))
}
