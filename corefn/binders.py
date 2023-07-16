from corefn.literals import Boolean, Float, Int, String


class Binder(object):
    def __repr__(self):
        raise NotImplementedError()

    def eval(self, interpreter, to_match, frame):
        raise NotImplementedError()


class VarBinder(Binder):
    def __init__(self, name):
        self.name = name

    def eval(self, interpreter, to_match, frame):
        return Match({self.name: to_match})

    def __repr__(self):
        return str(self.name)


class StringLiteralBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        if not isinstance(to_match, String):
            raise TypeError("Expected String got: " + to_match.__repr__())
        if self.value == to_match.value:
            return empty_match
        else:
            return no_match

    def __repr__(self):
        return str(self.value)


class IntBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        if not isinstance(to_match, Int):
            raise TypeError("Expected Int got: " + to_match.__repr__())
        elif self.value == to_match.value:
            return empty_match
        else:
            return no_match

    def __repr__(self):
        return str(self.value)


class FloatBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        if not isinstance(to_match, Float):
            raise TypeError("Expected Float got: " + to_match.__repr__())
        elif self.value == to_match.value:
            return empty_match
        else:
            return no_match

    def __repr__(self):
        raise NotImplementedError()


class BoolBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        if not isinstance(to_match, Boolean):
            raise TypeError("expected Boolean got: " + to_match.__repr__())
        elif self.value == to_match.value:
            return empty_match
        else:
            return no_match

    def __repr__(self):
        if self.value:
            return "True"
        else:
            return "False"


class RecordBinder(Binder):
    def __init__(self, record):
        self.record = record

    def eval(self, interpreter, to_match, frame):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()


class ArrayLiteralBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()


class ConstructorBinder(Binder):
    def __init__(self, binders):
        self.binders = binders

    def eval(self, interpreter, to_match, frame):
        matches = [b.eval(interpreter, to_match, frame) for b in self.binders]
        new_frame = {}
        for match in matches:
            if isinstance(match, Match):
                new_frame.update(match.frame)
            else:
                return no_match
        return Match(new_frame)

    def __repr__(self):
        return "<ConstructorBinder>"


class NullBinder(Binder):
    def eval(self, interpreter, to_match, frame):
        return empty_match

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


class MatchInterface(object):
    pass


class Match(MatchInterface):
    def __init__(self, frame):
        self.frame = frame


class NoMatch(MatchInterface):
    def __init__(self):
        pass


no_match = NoMatch()
empty_match = Match({})
