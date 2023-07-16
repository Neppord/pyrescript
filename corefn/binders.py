class Binder(object):
    def __repr__(self):
        raise NotImplementedError()

    def eval(self, interpreter, to_match, frame):
        raise NotImplementedError()


class VarBinder(Binder):
    def __init__(self, name):
        self.name = name

    def eval(self, interpreter, to_match, frame):
        return True, {self.name: to_match}

    def __repr__(self):
        return str(self.name)


class StringLiteralBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        return self.value == to_match.eval(interpreter, frame).value, {}

    def __repr__(self):
        return str(self.value)


class IntBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        return self.value == to_match.eval(interpreter, frame).value, {}

    def __repr__(self):
        return str(self.value)


class FloatBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        return self.value == to_match.eval(interpreter, frame).value, {}

    def __repr__(self):
        raise NotImplementedError()


class BoolBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        result = self.value == to_match.value
        return result, {}

    def __repr__(self):
        if self.value:
            return "True"
        else:
            return "False"


class RecordBinder(Binder):
    def __init__(self, record):
        self.record = record

    def eval(self, interpreter, to_match, frame):
        return self.record.obj == to_match.obj, {}

    def __repr__(self):
        return self.record.__repr__()


class ArrayLiteralBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        return self.value == to_match.eval(interpreter, frame).value, {}

    def __repr__(self):
        raise NotImplementedError()


class ConstructorBinder(Binder):
    def __init__(self, binders):
        self.binders = binders

    def eval(self, interpreter, to_match, frame):
        frames = [b.eval(interpreter, to_match, frame) for b in self.binders]
        new_frame = {}
        for r, f in frames:
            if r:
                new_frame.update(f)
            else:
                return False, {}
        return True, new_frame

    def __repr__(self):
        return "<ConstructorBinder>"


class NullBinder(Binder):
    def eval(self, interpreter, to_match, frame):
        return True, {}

    def __repr__(self):
        return "_"


class ArrayBinder(Binder):
    def __repr__(self):
        raise NotImplementedError()


class NamedBinder(Binder):
    def __init__(self, name, binder):
        self.name = name
        self.binder = binder

    def __repr__(self):
        raise NotImplementedError()
