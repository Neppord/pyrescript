import os.path
from subprocess import check_call

from purescript.corefn.abs import Abs
from purescript.corefn.expression import App
from purescript.corefn.literals import String, Int
from purescript.corefn.parsing import load_module
from purescript.corefn.var import LocalVar
from purescript.bytecode import Bytecode, Apply, LoadConstant, LoadLocal, LoadExternal
from purescript.bytecode.interpreter import BytecodeInterpreter
from purescript.bytecode.emitter import Emitter


def test_hello_world(capsys):
    bytecode = Bytecode("main")
    bytecode.constants = [String("hello world")]
    bytecode.opcodes = [
        LoadConstant(0),
        LoadExternal('Effect.Console', 'log'),
        Apply(),
    ]
    interpreter = BytecodeInterpreter({}, {})
    effect = interpreter.interpret(bytecode)
    effect.run_effect(None)
    assert capsys.readouterr().out == "hello world\n"


def test_lambda():
    bytecode = Bytecode("foo")
    emitter = Emitter(bytecode)
    ast = App(Abs("n", LocalVar("n")), Int(42))
    emitter.emit(ast)
    interpreter = BytecodeInterpreter({}, {})
    answer = interpreter.interpret(bytecode)
    assert answer == Int(42)


def test_e2e(monkeypatch, capsys):
    monkeypatch.chdir("../e2e/fizz-buzz")
    check_call(
        ["spago", "build", "--purs-args", "--codegen corefn"],
        shell=True
    )
    capsys.readouterr()
    module = load_module("Main")
    bytecode = Bytecode("Main")
    Emitter(bytecode).emit(module)
    interpreter = BytecodeInterpreter({'Main': bytecode}, {})
    effect = interpreter.interpret(bytecode.decl("main"))
    while isinstance(effect, Bytecode):
        effect = interpreter.interpret(effect)
    effect.run_effect(None)
    assert capsys.readouterr().out == ""
