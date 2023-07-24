from corefn.expression import App, Let
from corefn.literals import Int, Box
from corefn.var import LocalVar


class ByteCode(object):
    """
    represent a compiled piece of the program
    """

    def __init__(self, name):
        self.name = name
        self.opcodes = []
        self.constants = []

    def emit_declaration(self, name, bytecode):
        self.opcodes.append(Declaration(name, bytecode))

    def emit_apply(self):
        self.opcodes.append(Apply())

    def emit_load_constant(self, constant):
        for index, c in enumerate(self.constants):
            if c == constant:
                self.opcodes.append(LoadConstant(index))
                return
        self.opcodes.append(LoadConstant(len(self.constants)))
        self.constants.append(constant)

    def emit_load_declaration(self, name):
        self.opcodes.append(LoadDeclaration(name))


class Emitter(object):
    def __init__(self, bytecode):
        self.bytecode = bytecode

    def emit(self, ast):
        if isinstance(ast, Box):
            self.bytecode.emit_load_constant(ast)
        elif isinstance(ast, Let):
            for name, _ast in ast.binds.items():
                bytecode = ByteCode(name)
                emitter = Emitter(bytecode)
                emitter.emit(_ast)
                self.bytecode.emit_declaration(name, emitter.bytecode)
            self.emit(ast.expression)
        elif isinstance(ast, LocalVar):
            self.bytecode.emit_load_declaration(ast.name)
        else:
            NotImplementedError("%r" % ast)

class OpCode(object):
    """
    represent an operation code in the vm
    """
    pass


class Declaration(OpCode):
    def __init__(self, name, bytecode):
        self.name = name
        self.bytecode = bytecode


class Apply(OpCode):
    pass


class LoadConstant(OpCode):
    def __init__(self, index):
        self.index = index

    def __eq__(self, other):
        return isinstance(other, LoadConstant) and other.index == self.index


class LoadDeclaration(OpCode):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, LoadDeclaration) and other.name == self.name

