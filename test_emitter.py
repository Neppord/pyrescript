from corefn.expression import Let
from corefn.var import LocalVar
from purescript.bytecode import Emitter, Bytecode, Declaration, LoadDeclaration
from corefn.literals import Int, String
from purescript.bytecode import LoadConstant


def test_constant():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    emitter.emit(Int(42))
    emitter.emit(String("hello world"))
    emitter.emit(Int(42))
    assert bytecode.constants == [Int(42), String("hello world")]
    assert bytecode.opcodes == [LoadConstant(0), LoadConstant(1), LoadConstant(0)]


def test_declaration():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    emitter.emit(Let({"x": Int(42)}, LocalVar("x")))
    x_declaration, x_var = bytecode.opcodes
    assert isinstance(x_declaration, Declaration)
    assert x_declaration.name == "x"
    assert x_declaration.bytecode.name == "x"
    x_bytecode = x_declaration.bytecode
    assert x_bytecode.constants == [Int(42)]
    assert x_var == LoadDeclaration("x")

