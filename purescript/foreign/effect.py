from purescript.bytecode import Bytecode
from purescript.corefn.value import Closure, NativeX


def bindE(a, atob):
    bytecode = Bytecode("$bindE")
    bytecode.emit_load_constant(a)
    bytecode.emit_apply()
    bytecode.emit_load_constant(atob)
    bytecode.emit_apply()
    bytecode.emit_apply()
    return Closure({}, bytecode)


def pureE(x):
    bytecode = Bytecode("$pureE")
    bytecode.emit_load_constant(x)
    return Closure({}, bytecode)


exports = {
    'pureE': NativeX(pureE, 1, []),
    'bindE': NativeX(bindE, 2, []),
}
