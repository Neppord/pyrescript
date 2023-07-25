import pprint

from corefn.abs import Abs
from corefn.binders import BoolBinder, VarBinder, NullBinder
from corefn.case import Case, Alternative
from corefn.expression import Let, App
from corefn.var import LocalVar
from purescript.bytecode import Bytecode, Declaration, LoadLocal, Apply, StoreLocal, Duplicate, JumpAbsoluteIfNotEqual, \
    Pop, JumpAbsolute
from corefn.literals import Int, String, Boolean
from purescript.bytecode import LoadConstant
from purescript.bytecode.emitter import Emitter


def test_constant():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    emitter.emit(Int(42))
    emitter.emit(String("hello world"))
    emitter.emit(Int(42))
    assert bytecode.constants == [Int(42), String("hello world")]
    assert bytecode.opcodes == [LoadConstant(0), LoadConstant(1), LoadConstant(0)]


def test_let():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    emitter.emit(Let({"x": Int(42)}, LocalVar("x")))
    assert bytecode.opcodes == [LoadConstant(0), StoreLocal('x'), LoadLocal('x')]


def test_apply():
    bytecode = Bytecode("foo")
    emitter = Emitter(bytecode)
    ast = App(Abs("n", LocalVar("n")), Int(42))
    emitter.emit(ast)
    assert bytecode.opcodes == [
        LoadConstant(0),
        Declaration('\\n -> ', Bytecode('\\n -> ', [
            StoreLocal('n'),
            LoadLocal('n')
        ])),
        Apply()
    ]


def test_case_boolean_binder():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    ast = Case(
        [Boolean(True)],
        [Alternative(
            [BoolBinder(True)],
            String("Hello World")
        ),
            Alternative(
                [BoolBinder(False)],
                String("Goodbye World")
            )
        ]
    )
    emitter.emit(ast)
    assert bytecode.opcodes == [
        LoadConstant(0),
        Duplicate(),
        LoadConstant(0),
        JumpAbsoluteIfNotEqual(7),
        Pop(),
        LoadConstant(1),
        JumpAbsolute(13),
        Duplicate(),
        LoadConstant(2),
        JumpAbsoluteIfNotEqual(13),
        Pop(),
        LoadConstant(3),
        JumpAbsolute(13),
    ]


def test_case_var_binder():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    ast = Case(
        [Boolean(True)],
        [Alternative([VarBinder("n")], LocalVar("n"))]
    )
    emitter.emit(ast)
    assert bytecode.opcodes == [
        LoadConstant(0),
        StoreLocal('n'),
        LoadLocal('n'),
        JumpAbsolute(4)
    ]


def test_case_bool_and_null_binder():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    ast = Case(
        [Boolean(False)],
        [
            Alternative([BoolBinder(True)], String("skip")),
            Alternative([NullBinder()], String("take"))
        ]
    )
    emitter.emit(ast)
    assert bytecode.opcodes == [
        LoadConstant(0),
        Duplicate(),
        LoadConstant(1),
        JumpAbsoluteIfNotEqual(7),
        Pop(),
        LoadConstant(2),
        JumpAbsolute(10),
        Pop(),
        LoadConstant(3),
        JumpAbsolute(10),
    ]
