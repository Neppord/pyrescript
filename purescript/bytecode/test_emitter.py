import pprint

from purescript.bytecode.opcode import MakeData, GuardValue, GuardConstructor
from purescript.corefn.abs import Abs, Constructor
from purescript.corefn.binders import BoolBinder, VarBinder, NullBinder, ConstructorBinder
from purescript.corefn.case import Case, Alternative, GuardedAlternative
from purescript.corefn.expression import Let, App
from purescript.corefn.var import LocalVar
from purescript.bytecode import Bytecode, Declaration, LoadLocal, Apply, StoreLocal, Duplicate, JumpAbsoluteIfNotEqual, \
    Pop, JumpAbsolute, LoadConstant
from purescript.corefn.literals import Int, String, Boolean
from purescript.bytecode.emitter import Emitter


def test_constant():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    emitter.emit(Int(42))
    emitter.emit(String("hello world"))
    emitter.emit(Int(42))
    assert bytecode.constants == [Int(42), String("hello world")]
    assert bytecode.opcodes == [LoadConstant(0), LoadConstant(1), LoadConstant(0)]


def test_make_data():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    ast = App(Constructor("Just", ["a"]), Int(42))
    emitter.emit(ast)
    assert bytecode.constants == [Int(42)]
    assert bytecode.opcodes == [LoadConstant(0), MakeData("Just", 1), Apply()]


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
    assert bytecode.constants == [
        Int(42),
        Bytecode('\\n -> ', [StoreLocal('n'), LoadLocal('n')])
    ]
    assert bytecode.opcodes == [
        LoadConstant(0),
        LoadConstant(1),
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
        GuardValue(Boolean(True), 4),
        LoadConstant(1),
        JumpAbsolute(7),
        GuardValue(Boolean(False), 7),
        LoadConstant(2),
        JumpAbsolute(7),
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


def test_case_constructor():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    ast = Case(
        [App(Constructor("Box", ["a"]), Int(42))],
        [Alternative([ConstructorBinder("Main", "Box", [VarBinder("n")])], LocalVar("n"))]
    )
    emitter.emit(ast)
    assert bytecode.opcodes == [
        LoadConstant(0),
        MakeData('Box', 1),
        Apply(),
        GuardConstructor('Box', 7),
        StoreLocal('n'),
        LoadLocal('n'),
        JumpAbsolute(7)
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
        GuardValue(Boolean(True), 4),
        LoadConstant(1),
        JumpAbsolute(7),
        Pop(),
        LoadConstant(2),
        JumpAbsolute(7),
    ]


def test_guarded():
    bytecode = Bytecode("Main")
    emitter = Emitter(bytecode)
    ast = Case(
        [Boolean(False)],
        [
            GuardedAlternative([VarBinder("n")], [(LocalVar("n"), String("skip"))]),
            Alternative([NullBinder()], String("take"))
        ]
    )
    emitter.emit(ast)
    assert bytecode.opcodes == [LoadConstant(0),
         StoreLocal('n'),
         LoadLocal('n'),
         GuardValue(Boolean(True), 6),
         LoadConstant(1),
         JumpAbsolute(10),
         JumpAbsolute(10),
         Pop(),
         LoadConstant(2),
         JumpAbsolute(10)
    ]
