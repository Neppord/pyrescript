from types import FunctionType

from corefn.expression import Expression


class Box(Expression):

    def interpret(self, interpreter, frame):
        return self


class Object(Box):
    def __init__(self, obj):
        self.obj = obj

    def interpret(self, interpreter, frame):
        return Object({k: e.interpret(interpreter, frame) for k, e in self.obj.items()})

    def __repr__(self):
        key_value_pairs = []
        for field_name, expression in self.obj.items():
            expression_as_text = expression.__repr__()
            key_value_pair = field_name + ": " + expression_as_text
            key_value_pairs.append(key_value_pair)
        return "{" + ", ".join(key_value_pairs) + "}"


class Array(Box):
    def __init__(self, array):
        assert isinstance(array, list)
        self.array = array

    def __repr__(self):
        return "[" + ", ".join([a.__repr__() for a in self.array]) + "]"

    def interpret(self, interpreter, frame):
        return Array([e.interpret(interpreter, frame) for e in self.array])


class Int(Box):
    def __init__(self, value):
        """:type value: int"""
        assert isinstance(value, int)
        self.value = value

    def __repr__(self):
        return str(self.value)


class String(Box):
    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def __repr__(self):
        if '"' in self.value:
            return '"""' + self.value + '"""'
        else:
            return '"' + self.value + '"'


class Float(Box):
    def __init__(self, value):
        assert isinstance(value, float)
        self.value = value

    def __repr__(self):
        return str(self.value)


class Boolean(Box):
    def __init__(self, value):
        assert isinstance(value, bool)
        self.value = value

    def __repr__(self):
        return "true" if self.value else "false"


class Null(Box):
    def __init__(self):
        pass

    def __repr__(self):
        return "null"


nullLiteral = Null()


class Effect(Box):

    def __init__(self, effect):
        assert isinstance(effect, Expression)
        self.effect = effect

    def run_effect(self, interpreter):
        return self.effect.interpret(interpreter, {})

    def __repr__(self):
        return "Effect (%s)" % self.effect.__repr__()


class Bound(Box):
    def __init__(self, function):
        assert isinstance(function, FunctionType)
        self.function = function

    def interpret(self, interpreter, frame):
        return self.function()

    def __repr__(self):
        return "<native>"


class Bound1(Box):
    def __init__(self, function, x1):
        assert isinstance(function, FunctionType)
        self.function = function
        self.x1 = x1

    def interpret(self, interpreter, frame):
        return self.function(self.x1)

    def __repr__(self):
        return "<native> (%s)" % self.x1.__repr__()


class Bound2(Box):
    def __init__(self, function, x1, x2):
        assert isinstance(function, FunctionType)
        self.function = function
        self.x1 = x1
        self.x2 = x2

    def interpret(self, interpreter, frame):
        return self.function(self.x1, self.x2)

    def __repr__(self):
        return "<native> (%s) (%a)" % (self.x1.__repr__(), self.x2.__repre__())

