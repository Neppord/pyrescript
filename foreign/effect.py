from corefn.abs import Foreign, AbsInterface, Native2, Native1, BoundNative2, BoundBoundNative2, NativeX
from corefn.literals import Effect, Bound
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


bindE = Native2(bindE_)
pureE = Native1(lambda i, x: Effect(x))
