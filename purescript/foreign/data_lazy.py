from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Box


class Defered(Box):

    def __init__(self, thunk):
        self.thunk = thunk
        self.value = None

    def force(self):
        raise NotImplementedError("what to do here!?")

    def __repr__(self):
        if self.value:
            return "Defered (%s)" % self.value.__repr__()
        else:
            return "Defered (%s)" % self.thunk.__repr__()


def _defer(thunk):
    return Defered(thunk)


def _force(deferd):
    assert isinstance(deferd, Defered)
    return deferd.force()


exports = {
    'defer': NativeX(_defer, 1, []),
    'force': NativeX(_force, 1, [])
}
