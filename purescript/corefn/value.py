from purescript.corefn import Expression


class Box(Expression):

    def eval(self, interpreter, frame):
        return self


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


class Data(Box):

    def __init__(self, name, length, members):
        self.name = name
        self.length = length
        self.members = members

    def __repr__(self):
        if self.members:
            return "%s %s" % (self.name, " ".join([m.__repr__() for m in self.members]))
        else:
            return self.name

    def __eq__(self, other):
        return (
                isinstance(other, Data) and
                other.name == self.name and
                other.length == self.length and
                other.members == self.members
        )


class Unit(Box):
    def __init__(self):
        pass

    def __repr__(self):
        return "unit"

    def __eq__(self, other):
        return isinstance(other, Unit) and other.value == self.value


unit = Unit()


class Closure(Box):
    def __init__(self, vars_, bytecode):
        self.bytecode = bytecode
        self.vars = vars_

    def __repr__(self):
        return "Closure(%s, %s)" % (self.vars.__repr__(), self.bytecode.__repr__())


class NativeX(Box):
    def __init__(self, native, x, arguments):
        self.x = x
        self.native = native
        self.arguments = arguments
        assert x >= len(arguments)

    def __repr__(self):
        return "NativeX(%s, %s, %s)" % (
            self.native.__name__,
            self.x,
            self.arguments.__repr__()
        )
