import glob
import os.path
from subprocess import check_call

import pytest

from purescript.bytecode import Bytecode, Apply, LoadConstant, LoadExternal
from purescript.bytecode.emitter import Emitter
from purescript.bytecode.interpreter import BytecodeInterpreter, BaseFrame
from purescript.corefn.abs import Abs
from purescript.corefn.expression import App
from purescript.corefn.value import String, Int, NativeX, Closure
from purescript.corefn.var import LocalVar


def test_hello_world(capsys):
    bytecode = Bytecode("main")
    bytecode.constants = [String("hello world")]
    bytecode.opcodes = [
        LoadConstant(0),
        LoadExternal('Effect.Console', 'log'),
        Apply(),
    ]
    interpreter = BytecodeInterpreter()
    effect = interpreter.interpret(bytecode)
    while effect:
        if isinstance(effect, Closure):
            frame = BaseFrame(effect.bytecode, 0, effect.vars)
            effect = interpreter.interpret(effect.bytecode, frame)
        elif isinstance(effect, NativeX):
            effect = effect.native(*effect.arguments)
        else:
            break
    assert capsys.readouterr().out == "hello world\n"


def test_module():
    hello_world = Bytecode("hello_world")
    hello_world.emit_load_constant(String("hello world"))

    module = Bytecode("Main")
    module.emit_declaration(hello_world)

    interpreter = BytecodeInterpreter()
    frame = BaseFrame(module, 0, {})
    interpreter.interpret(module, frame)
    assert frame.vars == {"hello_world": String("hello world")}


def test_lambda():
    bytecode = Bytecode("foo")
    emitter = Emitter(bytecode)
    ast = App(Abs("n", LocalVar("n")), Int(42))
    emitter.emit(ast)
    interpreter = BytecodeInterpreter()
    answer = interpreter.interpret(bytecode)
    assert answer == Int(42)


dirname = os.path.dirname(__file__)
glob_expression = os.path.join(dirname, "..", "..", "e2e", "*", "expected.txt")
test_directories = []
for path in glob.glob(glob_expression):
    directory = os.path.dirname(os.path.relpath(path))
    example_name = os.path.basename(directory)
    test_directories.append(pytest.param(directory, id=example_name))


@pytest.mark.parametrize("test_directory", test_directories)
def test_e2e(test_directory, monkeypatch, capsys):
    monkeypatch.chdir(test_directory)
    check_call(
        ["spago", "build", "--purs-args", "--codegen corefn"],
        shell=True
    )
    capsys.readouterr()
    interpreter = BytecodeInterpreter()
    effect = interpreter.load_module("Main")["main"]
    while effect:
        if isinstance(effect, NativeX):
            effect = effect.native(*effect.arguments)
        elif isinstance(effect, Closure):
            vars_ = effect.vars
            frame = BaseFrame(effect.bytecode, 0, vars_)
            effect = interpreter.interpret(effect.bytecode, frame)
        else:
            break
    with open("expected.txt") as f:
        expected = f.read()
    assert capsys.readouterr().out == expected
