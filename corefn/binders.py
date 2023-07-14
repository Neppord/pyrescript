class VarBinder(object):
    def __init__(self, name):
        self.name = name

    def interpret(self, interpreter, to_match, frame):
        return True, {self.name: to_match}


class LiteralBinder(object):
    def __init__(self, value):
        self.value = value

    def interpret(self, interpreter, to_match, frame):
        return self.value == interpreter.expression(to_match, frame), {}


class ConstructorBinder(object):
    def __init__(self, binders):
        self.binders = binders

    def interpret(self, interpreter, to_match, frame):
        frames = [b.interpret(interpreter, to_match, frame) for b in self.binders]
        new_frame = {}
        for r, f in frames:
            if r:
                new_frame.update(f)
            else:
                return False, {}
        return True, new_frame


class NullBinder(object):
    def interpret(self, interpreter, to_match, frame):
        return True, {}


class ArrayBinder(object):
    pass


class NamedBinder(object):
    def __init__(self, name, binder):
        self.name = name
        self.binder = binder
