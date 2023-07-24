import corefn
from corefn import load_python_foreign, ModuleInterface
from corefn.abs import Native1
from corefn.expression import App, Let
from corefn.literals import Int, Box
from corefn.var import LocalVar


class Bytecode(object):
    """
    represent a compiled piece of the program
    """

    def __init__(self, name):
        self.name = name
        self.opcodes = []
        self.constants = []

    def emit_declaration(self, name, bytecode):
        self.opcodes.append(Declaration(name, bytecode))

    def emit_native_call(self, native, number_of_args):
        self.opcodes.append(NativeCall(native, number_of_args))

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

    def decl(self, name):
        for opcode in self.opcodes:
            if isinstance(opcode, Declaration) and opcode.name == name:
                return opcode.bytecode
        raise KeyError(name)


class Emitter(object):
    def __init__(self, bytecode):
        self.bytecode = bytecode

    def emit(self, ast):
        if isinstance(ast, Box):
            self.bytecode.emit_load_constant(ast)
        elif isinstance(ast, Let):
            for name, _ast in ast.binds.items():
                bytecode = Bytecode(name)
                emitter = Emitter(bytecode)
                emitter.emit(_ast)
                self.bytecode.emit_declaration(name, emitter.bytecode)
            self.emit(ast.expression)
        elif isinstance(ast, LocalVar):
            self.bytecode.emit_load_declaration(ast.name)
        elif isinstance(ast, ModuleInterface):
            for name, _ast in ast.declarations().items():
                bytecode = Bytecode(name)
                emitter = Emitter(bytecode)
                emitter.emit(_ast)
                self.bytecode.emit_declaration(name, emitter.bytecode)
        elif isinstance(ast, corefn.Declaration):
            self.emit(ast.expression)
        elif isinstance(ast, Native1):
            self.bytecode.emit_native_call(ast.native, 1)
        else:
            raise NotImplementedError("%r" % ast)


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


class LoadExternal(OpCode):
    def __init__(self, module, name):
        self.module = module
        self.name = name

    def __eq__(self, other):
        return (
                isinstance(other, LoadExternal)
                and other.module == self.module
                and other.name == self.name
        )


class NativeCall(OpCode):
    def __init__(self, native, number_of_args):
        self.native = native
        self.number_of_args = number_of_args

    def __eq__(self, other):
        return (
                isinstance(other, NativeCall) and
                other.native == self.native and
                other.number_of_args == self.number_of_args
        )


class BytecodeInterpreter(object):

    def interpret(self, bytecode, stack=None):
        pc = 0
        if not stack:
            stack = []
        modules = []
        while 1:
            if len(bytecode.opcodes) <= pc:
                return stack.pop()
            opcode = bytecode.opcodes[pc]
            if isinstance(opcode, LoadConstant):
                stack.append(bytecode.constants[opcode.index])
            elif isinstance(opcode, LoadExternal):
                foreign_module = load_python_foreign(opcode.module)
                module_bytecode = Bytecode(opcode.module)
                Emitter(module_bytecode).emit(foreign_module)
                decl = module_bytecode.decl(opcode.name)
                stack.append(decl)
            elif isinstance(opcode, Apply):
                func = stack.pop()
                ret = self.interpret(func, stack)
                stack.append(ret)
            elif isinstance(opcode, NativeCall):
                arg = stack.pop()
                stack.append(opcode.native(None, arg))
            else:
                raise NotImplementedError(opcode)
            pc += 1
