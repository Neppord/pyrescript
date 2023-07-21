import interpreter
from corefn.abs import Native1, AbsInterface, AbsWithFrame
from corefn.literals import Effect


def _unsafe_partial(i, value):
    if isinstance(value, Effect):
        return value.run_effect(i)
    else:
        return value


exports = {
    '_unsafePartial': Native1(_unsafe_partial)
}
