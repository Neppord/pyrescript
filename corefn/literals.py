from corefn.expression import Expression


class Literal(Expression):

    def interpret(self, interpreter, frame):
        return self


class ObjectLiteral(Literal):
    def __init__(self, obj):
        self.obj = obj

    def interpret(self, interpreter, frame):
        return ObjectLiteral({k: e.interpret(interpreter, frame) for k, e in self.obj.items()})
    def __repr__(self):
        key_value_pairs = []
        for field_name, expression in self.obj.items():
            expression_as_text = expression.__repr__()
            key_value_pair = field_name + ": " + expression_as_text
            key_value_pairs.append(key_value_pair)
        return "{" + ", ".join(key_value_pairs) + "}"


class ArrayLiteral(Literal):
    def __init__(self, array):
        self.array = array

    def __repr__(self):
        return "[" + ", ".join([a.__repr__() for a in self.array]) + "]"

    def interpret(self, interpreter, frame):
        return ArrayLiteral([ e.interpret(interpreter, frame) for e in self.array])


class IntLiteral(Literal):
    def __init__(self, value):
        """:type value: int"""
        self.value = value

    def __repr__(self):
        return str(self.value)


class StringLiteral(Literal):
    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def __repr__(self):
        if '"' in self.value:
            return '"""' + self.value + '"""'
        else:
            return '"' + self.value + '"'


class FloatLiteral(Literal):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class BoolLiteral(Literal):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "true" if self.value else "false"


class NullLiteral(Literal):
    def __init__(self):
        pass

    def __repr__(self):
        return "null"


nullLiteral = NullLiteral()
