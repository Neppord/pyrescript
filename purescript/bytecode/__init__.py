from purescript.bytecode.opcode import Declaration, Apply, Duplicate, Pop, LoadConstant, LoadLocal, AccessField, \
    AssignField, LoadExternal, StoreLocal, NativeCall, JumpAbsoluteIfNotEqual, JumpAbsolute, MakeData, GuardValue, \
    GuardConstructor, Stash, RestoreStash, DropStash


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

    def emit_declaration(self, bytecode):
        self.emit_load_constant(bytecode)
        self.emit_apply()
        self.emit_store(bytecode.name)

    def emit_store(self, name):
        self.opcodes.append(StoreLocal(name))

    def emit_guard_value(self, value):
        guard = GuardValue(value, -1)
        self.opcodes.append(guard)
        return guard

    def emit_guard_constructor(self, name):
        guard = GuardConstructor(name, -1)
        self.opcodes.append(guard)
        return guard

    def emit_access_field(self, name):
        self.opcodes.append(AccessField(name))

    def emit_assign_field(self, name):
        self.opcodes.append(AssignField(name))

    def emit_make_data(self, name, length):
        self.opcodes.append(MakeData(name, length))

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

    def emit_stash(self):
        self.opcodes.append(Stash())

    def emit_restore_stash(self):
        self.opcodes.append(RestoreStash())

    def emit_drop_stash(self):
        self.opcodes.append(DropStash())

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

    def __repr__(self):
        return "Bytecode(%r, %r)" % (self.name, self.opcodes)

    def __eq__(self, other):
        return (
                isinstance(other, Bytecode) and
                other.name == self.name and
                other.opcodes == self.opcodes and
                other.constants == self.constants
        )
