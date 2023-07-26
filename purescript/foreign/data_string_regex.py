from purescript.corefn.abs import AbsInterface, NativeX
from purescript.corefn.literals import String, Box, Record, Boolean, Array
from rpython.rlib.rsre import rsre_re


class RegEx(Box):

    def __init__(self, expression, flags):
        self.flags = flags
        self.expression = expression

    def __repr__(self):
        return "RegEx(%s, %s)" % (
            self.expression.__repr__(),
            self.flags.__repr__()
        )

    def match(self, s):
        match = rsre_re.search(self.expression, s)
        if match:
            return [match.group()] + list(match.groups())
        else:
            return None


# TODO: check regex
def _regex_impl(i, left, right, s1, flags):
    assert isinstance(left, AbsInterface)
    assert isinstance(right, AbsInterface)
    assert isinstance(s1, String)
    assert isinstance(flags, String)
    return right.call_abs(i, RegEx(s1.value, flags))


def _match(i, just, nothing, re, s2):
    assert isinstance(just, AbsInterface)
    assert isinstance(re, RegEx)
    assert isinstance(s2, String)
    groups = re.match(s2.value)
    if groups:
        return just.call_abs(i, Array([
            nothing if g is None
            else just.call_abs(i, String(g))
            for g in groups
        ]))
    else:
        return nothing


exports = {
    'regexImpl': NativeX(_regex_impl, 4, []),
    '_match': NativeX(_match, 4, []),
    'showRegexImpl': NativeX(lambda i, r: String(str(r)), 1, []),
    'flagsImpl': NativeX(lambda i, r: r, 1, []),
}
