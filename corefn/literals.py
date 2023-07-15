from corefn.expression import Expression


class ObjectLiteral(Expression):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        key_value_pairs = []
        for field_name, expression in self.obj.items():
            expression_as_text = expression.__repr__()
            key_value_pair = field_name + ": " + expression_as_text
            key_value_pairs.append(key_value_pair)
        return "{" + ", ".join(key_value_pairs) + "}"

    def interpret(self, interpreter, frame):
        return self.obj


class ArrayLiteral(Expression):
    def __init__(self, array):
        self.array = array

    def __repr__(self):
        return "[" + ", ".join([a.__repr__() for a in self.array]) + "]"

    def interpret(self, interpreter, frame):
        return self.array


class IntLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def interpret(self, interpreter, frame):
        return self.value


class StringLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if '"' in self.value:
            return '"""' + self.value + '"""'
        else:
            return '"' + self.value + '"'

    def interpret(self, interpreter, frame):
        return self.value


class FloatLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def interpret(self, interpreter, frame):
        return self.value


class BoolLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "true" if self.value else "false"

    def interpret(self, interpreter, frame):
        return self.value


class NullLiteral(Expression):
    def __init__(self):
        pass

    def __repr__(self):
        return "null"

    def interpret(self, interpreter, frame):
        return None


nullLiteral = NullLiteral()
