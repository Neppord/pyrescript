from purescript.corefn.abs import NativeX
from purescript.corefn.literals import Effect


def _unsafe_partial(value):
    if isinstance(value, Effect):
        return value.run_effect(i)
    else:
        return value


exports = {
    '_unsafePartial': NativeX(_unsafe_partial, 1, [])
}
