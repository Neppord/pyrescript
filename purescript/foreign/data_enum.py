from purescript.corefn.value import Char, Int, NativeX


def _to_char_code(c):
    assert isinstance(c, Char)
    return Int(ord(c.value))


exports = {
    'toCharCode': NativeX(_to_char_code, 1, [])
}
