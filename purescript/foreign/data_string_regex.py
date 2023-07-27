from purescript.corefn.abs import AbsInterface, NativeX
from purescript.corefn.value import String, Box, Record, Boolean, Array, Int
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

    def search(self, s):
        match = rsre_re.search(self.expression, s)
        if match is None:
            return -1
        else:
            return match.pos


# TODO: check regex
def _regex_impl(left, right, s1, flags):
    assert isinstance(left, AbsInterface)
    assert isinstance(right, AbsInterface)
    assert isinstance(s1, String)
    assert isinstance(flags, String)
    return right.call_abs(RegEx(s1.value, flags))


def _match(just, nothing, re, s2):
    assert isinstance(re, RegEx)
    assert isinstance(s2, String)
    groups = re.match(s2.value)
    if groups:
        return just(Array([
            nothing if g is None
            else just(String(g))
            for g in groups
        ]))
    else:
        return nothing


def _search(just, nothing, re, s):
    assert isinstance(re, RegEx)
    assert isinstance(s, String)
    index = re.search(s.value)
    if index == -1:
        return nothing
    else:
        return just(Int(index))


def _replaceBy(just, nothing, re, s):
    raise NotImplementedError()


def flagsImpl(r):
    assert isinstance(r, Record)

    return Record({
        "multiline": Boolean(False),
        "ignoreCase": Boolean(False),
        "global": Boolean(False),
        "dotAll": Boolean(False),
        "sticky": Boolean(False),
        "unicode": Boolean(False),
    })


exports = {
    'regexImpl': NativeX(_regex_impl, 4, []),
    '_match': NativeX(_match, 4, []),
    '_search': NativeX(_search, 4, []),
    '_replaceBy': NativeX(_replaceBy, 4, []),
    'showRegexImpl': NativeX(lambda r: String(str(r)), 1, []),
    'flagsImpl': NativeX(flagsImpl, 1, []),
}
