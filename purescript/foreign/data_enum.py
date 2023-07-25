from purescript.corefn.abs import Native1
from purescript.corefn.literals import Char, Int


def _to_char_code(i, c):
    assert isinstance(c, Char)
    return Int(ord(c.value))

exports = {
    'toCharCode': Native1(_to_char_code)
}