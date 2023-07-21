from types import FunctionType

from corefn.expression import Expression


class Box(Expression):

    def eval(self, interpreter, frame):
        return self


class Record(Box):
    def __init__(self, obj):
        self.obj = obj

    def eval(self, interpreter, frame):
        new_obj = {}
        for k, e in self.obj.items():
            new_obj[k] = e.eval(interpreter, frame)
        return Record(new_obj)

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

    def eval(self, interpreter, frame):
        return Array([e.eval(interpreter, frame) for e in self.array])


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


class Char(Box):
    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def __repr__(self):
        return "'" + self.value + "'"


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


class Unit(Box):
    def __init__(self):
        pass

    def __repr__(self):
        return "unit"


unit = Unit()


class Effect(Box):

    def __init__(self, effect):
        assert isinstance(effect, Expression)
        self.effect = effect

    def run_effect(self, interpreter):
        return self.effect.eval(interpreter, {})

    def __repr__(self):
        return "Effect (%s)" % self.effect.__repr__()


class Bound(Box):
    def __init__(self, function):
        assert isinstance(function, FunctionType)
        self.function = function

    def eval(self, interpreter, frame):
        return self.function()

    def __repr__(self):
        return "<native>"
