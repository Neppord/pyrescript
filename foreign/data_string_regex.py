from corefn.abs import AbsInterface, NativeX
from corefn.literals import String, Box


class RegEx(Box):

    def __init__(self, expression, flags):
        self.flags = flags
        self.expression = expression

    def __repr__(self):
        return "RegEx(%s, %s)" % (
            self.expression.__repr__(),
            self.flags.__repr__()
        )


# TODO: check regex
def _regex_impl(i, left, right, s1, s2):
    assert isinstance(left, AbsInterface)
    assert isinstance(right, AbsInterface)
    assert isinstance(s1, String)
    assert isinstance(s2, String)
    return right.call_abs(i, RegEx(s1.value, s2.value))


exports = {
    'regexImpl': NativeX(_regex_impl, 4, [])
}
