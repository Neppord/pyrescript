import glob
import os.path
import sys
from subprocess import check_call

import pytest

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
    fun = effect.effect
    fun.native(None, *fun.arguments)
    assert capsys.readouterr().out == "hello world\n"


def test_lambda():
    bytecode = Bytecode("foo")
    emitter = Emitter(bytecode)
    ast = App(Abs("n", LocalVar("n")), Int(42))
    emitter.emit(ast)
    interpreter = BytecodeInterpreter({}, {})
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
    module = load_module("Main")
    bytecode = Bytecode("Main")
    Emitter(bytecode).emit(module)
    interpreter = BytecodeInterpreter({'Main': bytecode}, {})
    effect = interpreter.interpret(bytecode.decl("main"))
    fun = effect.effect
    fun.native(None, *fun.arguments)
    with open("expected.txt") as f:
        expected = f.read()
    assert capsys.readouterr().out == expected
