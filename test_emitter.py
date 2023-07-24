from purescript.bytecode import Emitter, ByteCode
from corefn.literals import Int, String
from purescript.bytecode import LoadConstant


def test_constant():
    bytecode = ByteCode("Main")
    emitter = Emitter(bytecode)
    emitter.emit(Int(42))
    emitter.emit(String("hello world"))
    assert bytecode.constants == [Int(42), String("hello world")]
    assert bytecode.opcodes == [LoadConstant(0), LoadConstant(1)]
