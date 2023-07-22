
class ByteCode(object):
    """
    represent a compiled piece of the program
    """
    def __init__(self, name):
        self.name = name

class OpCode(object):
    """
    represent an operation code in the vm
    """
    pass


class Apply(OpCode):
    pass


class LoadConstant(OpCode):
    pass

class LoadVariable(OpCode):
    pass

class StoreVariable(OpCode):
    pass

