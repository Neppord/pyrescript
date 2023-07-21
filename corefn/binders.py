from corefn.abs import ConstructorInvocation
from corefn.literals import Boolean, Float, Int, String, Record


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


class CharLiteralBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        if not isinstance(to_match, Char):
            raise TypeError("Expected Char got: " + to_match.__repr__())
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
        assert isinstance(to_match, Record)
        frame = {}
        for k, b in self.record.items():
            if k not in to_match.obj:
                return no_match
            else:
                assert isinstance(b, Binder)
                match = b.eval(interpreter, to_match.obj[k], frame)
                if match == no_match:
                    return no_match
                else:
                    frame.update(match.frame)
        return Match(frame)

    def __repr__(self):
        return "{" + ", ".join([
            "%s:%s" % (k, v.__repr__())
            for k, v in self.record.items()
        ]) + "}"


class ArrayLiteralBinder(Binder):
    def __init__(self, value):
        self.value = value

    def eval(self, interpreter, to_match, frame):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()


class ConstructorBinder(Binder):
    def __init__(self, module_name, identifier, binders):
        self.module_name = module_name
        self.identifier = identifier
        self.binders = binders

    def eval(self, interpreter, to_match, frame):
        if isinstance(to_match, ConstructorInvocation):
            if to_match.name != self.identifier:
                return no_match
            matches = []
            arguments = to_match.arguments
            assert len(self.binders) == len(arguments)
            for i, binder in enumerate(self.binders):
                matches.append(binder.eval(interpreter, arguments[i], frame))
        else:
            matches = [b.eval(interpreter, to_match, frame) for b in self.binders]
        new_frame = {}
        for match in matches:
            if isinstance(match, Match):
                new_frame.update(match.frame)
            else:
                return no_match
        return Match(new_frame)

    def __repr__(self):
        return "%s.%s" % (self.module_name, self.identifier)


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
        return "%s@%s" % (self.name, self.binder.__repr__())


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
