from purescript.corefn.abs import AbsInterface, NativeX
from purescript.corefn.literals import Effect
from purescript.bytecode import Bytecode


def bindE__(i, a, atob):
    return atob.call_abs(i, a.run_effect(i)).run_effect(i)


def bindE_(interpreter, a, atob):
    if not isinstance(a, Effect):
        raise TypeError("expected Effect got: " + a.__repr__())
    if isinstance(atob, AbsInterface):
        return Effect(NativeX(bindE__, 2, [a, atob]))
    if isinstance(atob, Bytecode):
        effect = Bytecode("effect")
        effect.emit_load_constant(a)
        effect.emit_load_constant(atob)
        effect.emit_apply()
        return effect
    else:
        raise TypeError("expected Abs got: " + atob.__repr__())


exports = {
    'pureE': NativeX(lambda i, x: Effect(x), 1, []),
    'bindE': NativeX(bindE_, 2, []),
}
