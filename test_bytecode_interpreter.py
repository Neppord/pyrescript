from corefn.literals import String
from purescript.bytecode import Bytecode, Apply, LoadConstant, LoadDeclaration, BytecodeInterpreter, LoadExternal


def test_hello_world(capsys):
    bytecode = Bytecode("main")
    bytecode.constants = [String("hello world")]
    bytecode.opcodes = [
        LoadConstant(0),
        LoadExternal('Effect.Console', 'log'),
        Apply(),
    ]
    effect = BytecodeInterpreter().interpret(bytecode)
    effect.run_effect(None)
    assert capsys.readouterr().out == "hello world\n"
