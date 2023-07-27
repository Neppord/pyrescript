from purescript.bytecode import Bytecode, LoadLocal, Apply, StoreLocal, Duplicate, Pop, JumpAbsolute, LoadConstant
from purescript.bytecode.emitter import Emitter
from purescript.bytecode.opcode import MakeData, GuardValue, GuardConstructor, Stash, RestoreStash, DropStash
from purescript.corefn.abs import Abs, Constructor
from purescript.corefn.binders import BoolBinder, VarBinder, NullBinder, ConstructorBinder
from purescript.corefn.case import Case, Alternative, GuardedAlternative
from purescript.corefn.expression import Let, App
from purescript.corefn.value import Int, String, Boolean
from purescript.corefn.var import LocalVar


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
        Stash(),
        RestoreStash(),
        Duplicate(),
        GuardValue(Boolean(True), 7),
        LoadConstant(1),
        JumpAbsolute(12),
        RestoreStash(),
        Duplicate(),
        GuardValue(Boolean(False), 12),
        LoadConstant(2),
        JumpAbsolute(12),
        DropStash()
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
        Stash(),
        RestoreStash(),
        StoreLocal('n'),
        LoadLocal('n'),
        JumpAbsolute(6),
        DropStash()
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
        Stash(),
        RestoreStash(),
        GuardConstructor('Box', 9),
        StoreLocal('n'),
        LoadLocal('n'),
        JumpAbsolute(9),
        DropStash()
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
        Stash(),
        RestoreStash(),
        Duplicate(),
        GuardValue(Boolean(True), 7),
        LoadConstant(1),
        JumpAbsolute(11),
        RestoreStash(),
        Pop(),
        LoadConstant(2),
        JumpAbsolute(11),
        DropStash()
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
    assert bytecode.opcodes == [
        LoadConstant(0),
        Stash(),
        RestoreStash(),
        StoreLocal('n'),
        LoadLocal('n'),
        GuardValue(Boolean(True), 8),
        LoadConstant(1),
        JumpAbsolute(13),
        JumpAbsolute(13),
        RestoreStash(),
        Pop(),
        LoadConstant(2),
        JumpAbsolute(13),
        DropStash()
    ]
