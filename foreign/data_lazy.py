from corefn.abs import Native1, AbsWithFrame
from corefn.literals import Box


class Defered(Box):

    def __init__(self, thunk):
        self.thunk = thunk
        self.value = None

    def eval(self, interpreter, frame):
        return self

    def force(self, interpreter):
        if self.value is None:
            if isinstance(self.thunk, AbsWithFrame):
                self.value = self.thunk.fix_eval(interpreter, {})
            else:
                raise NotImplementedError("what to do here!?")
        return self.value

    def __repr__(self):
        if self.value:
            return "Defered (%s)" % self.value.__repr__()
        else:
            return "Defered (%s)" % self.thunk.__repr__()

def _defer(i, thunk):
    return Defered(thunk)


def _force(i, deferd):
    assert isinstance(deferd, Defered)
    return deferd.force(i)


exports = {
    'defer': Native1(_defer),
    'force': Native1(_force)
}
