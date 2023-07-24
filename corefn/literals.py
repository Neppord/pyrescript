from types import FunctionType

from corefn.expression import Expression


class Box(Expression):

    def eval(self, interpreter, frame):
        return self


class RecordLiteral(Expression):
    def __init__(self, obj):
        self.obj = obj

    def eval(self, interpreter, frame):
        new_obj = {}
        for k, e in self.obj.items():
            new_obj[k] = e.fix_eval(interpreter, frame)
        return Record(new_obj)

    def __repr__(self):
        key_value_pairs = []
        for field_name, expression in self.obj.items():
            expression_as_text = expression.__repr__()
            key_value_pair = field_name + ": " + expression_as_text
            key_value_pairs.append(key_value_pair)
        return "{" + ", ".join(key_value_pairs) + "}"


class Record(Box):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        key_value_pairs = []
        for field_name, expression in self.obj.items():
            expression_as_text = expression.__repr__()
            key_value_pair = field_name + ": " + expression_as_text
            key_value_pairs.append(key_value_pair)
        return "{" + ", ".join(key_value_pairs) + "}"

    def __eq__(self, other):
        return isinstance(other, Record) and other.obj == self.obj


class ArrayLiteral(Expression):
    def __init__(self, array):
        assert isinstance(array, list)
        self.array = array

    def __repr__(self):
        return "[" + ", ".join([a.__repr__() for a in self.array]) + "]"

    def eval(self, interpreter, frame):
        return Array([e.fix_eval(interpreter, frame) for e in self.array])


class Array(Box):
    def __init__(self, array):
        assert isinstance(array, list)
        self.array = array

    def __repr__(self):
        return "[" + ", ".join([a.__repr__() for a in self.array]) + "]"

    def __eq__(self, other):
        return isinstance(other, Array) and other.array == self.array


class Int(Box):
    def __init__(self, value):
        """:type value: int"""
        assert isinstance(value, int)
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, Int) and other.value == self.value


class String(Box):
    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def __repr__(self):
        if '"' in self.value:
            return '"""' + self.value + '"""'
        else:
            return '"' + self.value + '"'

    def __eq__(self, other):
        return isinstance(other, String) and other.value == self.value


class Char(Box):
    def __init__(self, value):
        assert isinstance(value, str)
        self.value = value

    def __repr__(self):
        return "'" + self.value + "'"

    def __eq__(self, other):
        return isinstance(other, Char) and other.value == self.value


class Float(Box):
    def __init__(self, value):
        assert isinstance(value, float)
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, Float) and other.value == self.value


class Boolean(Box):
    def __init__(self, value):
        assert isinstance(value, bool)
        self.value = value

    def __repr__(self):
        return "true" if self.value else "false"

    def __eq__(self, other):
        return isinstance(other, Boolean) and other.value == self.value


class Unit(Box):
    def __init__(self):
        pass

    def __repr__(self):
        return "unit"

    def __eq__(self, other):
        return isinstance(other, Unit) and other.value == self.value


unit = Unit()


class Effect(Box):

    def __init__(self, effect):
        assert isinstance(effect, Expression)
        self.effect = effect

    def run_effect(self, interpreter):
        return self.effect.fix_eval(interpreter, {})

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
