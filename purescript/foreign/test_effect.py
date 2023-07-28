from purescript.bytecode import Bytecode
from purescript.bytecode.interpreter import BytecodeInterpreter, BaseFrame
from purescript.corefn.value import Int, Closure
from purescript.foreign import foreign
from purescript.foreign.effect import pureE, bindE

value = Int(42)
effect_int = pureE(value)


def test_pureE():
    interpreter = BytecodeInterpreter()
    frame = BaseFrame(effect_int.bytecode, 0, effect_int.vars)
    actual = interpreter.interpret(effect_int.bytecode, frame)
    assert actual == value


def test_bindE():
    inc_bytecode = Bytecode("inc")
    inc_bytecode.emit_load_constant(Int(1))
    inc_bytecode.emit_load_constant(foreign['Data.Semiring']['intAdd'])
    inc_bytecode.emit_apply()
    inc_bytecode.emit_apply()
    inc_bytecode.emit_load_constant(foreign['Effect']['pureE'])
    inc_bytecode.emit_apply()
    inc_effect = Closure({}, inc_bytecode)
    bound_effect = bindE(bindE(effect_int, inc_effect), inc_effect)
    interpreter = BytecodeInterpreter()
    frame = BaseFrame(bound_effect.bytecode, 0, bound_effect.vars)
    actual = interpreter.interpret(bound_effect.bytecode, frame)
    assert actual == Int(44)
