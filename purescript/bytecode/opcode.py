class OpCode(object):
    """
    represent an operation code in the vm
    """
    pass


class Declaration(OpCode):
    """
    A declaration contains bytecode that should be interpreted and
     then assigned to the name of the declaration
    """

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
    """
    Calls the top of the stack:
    if it is a native function it calls it by applying the next item on the stack
    if it is a bytecode it calls it and let it handle the stack
    """

    def __repr__(self):
        return "Apply()"

    def __eq__(self, other):
        return isinstance(other, Apply)


class Duplicate(OpCode):
    """
    duplicate the top of the stack, used together with operations that consumes the top of the stack.
    """

    def __repr__(self):
        return "Duplicate()"

    def __eq__(self, other):
        return isinstance(other, Duplicate)


class Pop(OpCode):
    """
    Throws away the top of the stack
    """

    def __repr__(self):
        return "Pop()"

    def __eq__(self, other):
        return isinstance(other, Pop)


class LoadConstant(OpCode):
    """
    Loads constant from the constants area.
    """

    def __init__(self, index):
        self.index = index

    def __eq__(self, other):
        return isinstance(other, LoadConstant) and other.index == self.index

    def __repr__(self):
        return "LoadConstant(%s)" % self.index


class LoadLocal(OpCode):
    """
    Loads value from current scope (frame)
    """

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, LoadLocal) and other.name == self.name

    def __repr__(self):
        return "LoadLocal(%r)" % self.name


class AccessField(OpCode):
    """
    Replaces the top of the stack with the field from the record currently at the top of the stack
    """

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, AccessField) and other.name == self.name

    def __repr__(self):
        return "AccessField(%r)" % self.name


class AssignField(OpCode):
    """
    TODO: replace with immutable operation
    Assign the top of the stack value to the field of stack +1 that needs to be a record
    """

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, AssignField) and other.name == self.name

    def __repr__(self):
        return "AssignField(%r)" % self.name


class LoadExternal(OpCode):
    """
    Asks the interpreter to load and interpret `module`, and then grabs `name` from its scope
    """

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


class Lambda(OpCode):
    def __init__(self, bytecode):
        self.bytecode = bytecode

    def __eq__(self, other):
        return isinstance(other, Lambda) and other.bytecode == self.bytecode

    def __repr__(self):
        return "Lambda(%s)" % self.bytecode.__repr__()


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


class GuardValue(OpCode):
    def __init__(self, value, address):
        self.value = value
        self.address = address

    def __eq__(self, other):
        return (
                isinstance(other, GuardValue) and
                other.value == self.value and
                other.address == self.address
        )

    def __repr__(self):
        return "GuardValue(%s, %s)" % (self.value.__repr__(), self.address)


class GuardConstructor(OpCode):
    """
    Checks that the top of the stack is a data object with matching constructor name, otherwise puts it back and jumps
    if it matches it splices the members onto the stack in reverse order, with the first member at the top of the stack
    """

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __eq__(self, other):
        return (
                isinstance(other, GuardConstructor) and
                other.name == self.name and
                other.address == self.address
        )

    def __repr__(self):
        return "GuardConstructor(%s, %s)" % (self.name.__repr__(), self.address)


class JumpAbsolute(OpCode):
    def __init__(self, address):
        self.address = address

    def __eq__(self, other):
        return isinstance(other, JumpAbsolute) and other.address == self.address

    def __repr__(self):
        return "JumpAbsolute(%s)" % self.address


class MakeData(OpCode):

    def __init__(self, name, length):
        self.length = length
        self.name = name

    def __eq__(self, other):
        return (
                isinstance(other, MakeData) and
                other.name == self.name and
                other.length == self.length
        )

    def __repr__(self):
        return "MakeData(%s, %s)" % (self.name.__repr__(), self.length)


class Stash(OpCode):
    def __repr__(self):
        return "Stash()"

    def __eq__(self, other):
        return isinstance(other, Stash)


class RestoreStash(OpCode):
    def __repr__(self):
        return "RestoreStash()"

    def __eq__(self, other):
        return isinstance(other, RestoreStash)


class DropStash(OpCode):
    def __repr__(self):
        return "DropStash()"

    def __eq__(self, other):
        return isinstance(other, DropStash)
