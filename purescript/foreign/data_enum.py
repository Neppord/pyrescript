from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Char, Int


def _to_char_code(c):
    assert isinstance(c, Char)
    return Int(ord(c.value))


exports = {
    'toCharCode': NativeX(_to_char_code, 1, [])
}
