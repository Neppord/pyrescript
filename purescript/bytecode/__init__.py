from corefn.expression import App
from corefn.literals import Int, Box


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

