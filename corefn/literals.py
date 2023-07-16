from corefn.expression import Expression


class Box(Expression):

    def interpret(self, interpreter, frame):
        return self


class Object(Box):
    def __init__(self, obj):
        assert isinstance(obj, dict)
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
