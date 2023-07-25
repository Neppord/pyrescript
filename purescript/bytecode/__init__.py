class Bytecode(object):
    """
    represent a compiled piece of the program
    """

    def __init__(self, name, opcodes=None):
        self.name = name
        if opcodes:
            self.opcodes = opcodes
        else:
            self.opcodes = []
        self.constants = []

    def emit_declaration(self, name, bytecode):
        self.opcodes.append(Declaration(name, bytecode))

    def emit_store(self, name):
        self.opcodes.append(StoreLocal(name))

    def emit_access_field(self, name):
        self.opcodes.append(AccessField(name))

    def emit_assign_field(self, name):
        self.opcodes.append(AssignField(name))

    def emit_native_call(self, native, number_of_args):
        self.opcodes.append(NativeCall(native, number_of_args))

    def emit_jump_if_not_equal(self):
        jump_to = JumpAbsoluteIfNotEqual(-1)
        self.opcodes.append(jump_to)
        return jump_to

    def emit_jump(self):
        jump_to = JumpAbsolute(-1)
        self.opcodes.append(jump_to)
        return jump_to

    def emit_apply(self):
        self.opcodes.append(Apply())

    def emit_duplicate(self):
        self.opcodes.append(Duplicate())

    def emit_pop(self):
        self.opcodes.append(Pop())

    def emit_load_constant(self, constant):
        for index, c in enumerate(self.constants):
            if c == constant:
                self.opcodes.append(LoadConstant(index))
                return
        self.opcodes.append(LoadConstant(len(self.constants)))
        self.constants.append(constant)

    def emit_load_declaration(self, name):
        self.opcodes.append(LoadLocal(name))

    def emit_load_external(self, module_name, name):
        self.opcodes.append(LoadExternal(module_name, name))

    def decl(self, name):
        for opcode in self.opcodes:
            if isinstance(opcode, Declaration) and opcode.name == name:
                return opcode.bytecode
        raise KeyError(name)

    def __repr__(self):
        return "Bytecode(%r, %r)" % (self.name, self.opcodes)

    def __eq__(self, other):
        return (
                isinstance(other, Bytecode) and
                other.name == self.name and
                other.opcodes == self.opcodes and
                other.constants == self.constants
        )


class OpCode(object):
    """
    represent an operation code in the vm
    """
    pass


class Declaration(OpCode):
    def __init__(self, name, bytecode):
        self.name = name
        self.bytecode = bytecode

    def __repr__(self):
        return "Declaration(%r , %r)" % (self.name, self.bytecode)

    def __eq__(self, other):
        return (
                isinstance(other, Declaration) and
                other.name == self.name and
                other.bytecode == self.bytecode
        )


class Apply(OpCode):
    def __repr__(self):
        return "Apply()"

    def __eq__(self, other):
        return isinstance(other, Apply)


class Duplicate(OpCode):
    def __repr__(self):
        return "Duplicate()"

    def __eq__(self, other):
        return isinstance(other, Duplicate)


class Pop(OpCode):
    def __repr__(self):
        return "Pop()"

    def __eq__(self, other):
        return isinstance(other, Pop)


class LoadConstant(OpCode):
    def __init__(self, index):
        self.index = index

    def __eq__(self, other):
        return isinstance(other, LoadConstant) and other.index == self.index

    def __repr__(self):
        return "LoadConstant(%s)" % self.index


class LoadLocal(OpCode):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, LoadLocal) and other.name == self.name

    def __repr__(self):
        return "LoadLocal(%r)" % self.name


class AccessField(OpCode):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, AccessField) and other.name == self.name

    def __repr__(self):
        return "AccessField(%r)" % self.name


class AssignField(OpCode):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, AssignField) and other.name == self.name

    def __repr__(self):
        return "AssignField(%r)" % self.name


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

    def __repr__(self):
        return "LoadExternal(%s, %s)" % (
            self.module.__repr__(),
            self.name.__repr__()
        )


class StoreLocal(OpCode):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, StoreLocal) and other.name == self.name

    def __repr__(self):
        return "StoreLocal(%s)" % self.name.__repr__()


class NativeCall(OpCode):
    def __init__(self, native, number_of_args):
        self.native = native
        self.number_of_args = number_of_args

    def __repr__(self):
        return "NativeCall(%r, %r)" % (self.native.__name__, self.number_of_args)

    def __eq__(self, other):
        return (
                isinstance(other, NativeCall) and
                other.native == self.native and
                other.number_of_args == self.number_of_args
        )


class JumpAbsoluteIfNotEqual(OpCode):
    def __init__(self, address):
        self.address = address

    def __eq__(self, other):
        return isinstance(other, JumpAbsoluteIfNotEqual) and other.address == self.address

    def __repr__(self):
        return "JumpAbsoluteIfNotEqual(%s)" % self.address

class JumpAbsolute(OpCode):
    def __init__(self, address):
        self.address = address

    def __eq__(self, other):
        return isinstance(other, JumpAbsolute) and other.address == self.address

    def __repr__(self):
        return "JumpAbsolute(%s)" % self.address
