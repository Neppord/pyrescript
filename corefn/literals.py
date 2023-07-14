from corefn.expression import Expression


class ObjectLiteral(Expression):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return repr(self.obj)

    def interpret(self, interpreter, frame):
        return self.obj


class ArrayLiteral(Expression):
    def __init__(self, array):
        self.array = array

    def __repr__(self):
        return repr(self.array)

    def interpret(self, interpreter, frame):
        return self.array


class ValueLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def interpret(self, interpreter, frame):
        return self.value
