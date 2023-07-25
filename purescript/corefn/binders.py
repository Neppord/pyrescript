class Binder(object):
    def __repr__(self):
        raise NotImplementedError()


class VarBinder(Binder):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)


class StringLiteralBinder(Binder):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class CharLiteralBinder(Binder):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class IntBinder(Binder):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class FloatBinder(Binder):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        raise NotImplementedError()


class BoolBinder(Binder):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if self.value:
            return "True"
        else:
            return "False"


class RecordBinder(Binder):
    def __init__(self, record):
        self.record = record

    def __repr__(self):
        return "{" + ", ".join([
            "%s:%s" % (k, v.__repr__())
            for k, v in self.record.items()
        ]) + "}"


class ArrayLiteralBinder(Binder):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        items = ", ".join([b.__repr__() for b in self.value])
        return "[%s]" % items


class ConstructorBinder(Binder):
    def __init__(self, module_name, identifier, binders):
        self.module_name = module_name
        self.identifier = identifier
        self.binders = binders

    def __repr__(self):
        binders = " ".join([b.__repr__() for b in self.binders])
        return "%s.%s %s" % (self.module_name, self.identifier, binders)

class NewtypeBinder(Binder):
    def __init__(self, module_name, identifier, binders):
        self.module_name = module_name
        self.identifier = identifier
        self.binders = binders

    def __repr__(self):
        binders = " ".join([b.__repr__() for b in self.binders])
        return "%s.%s %s" % (self.module_name, self.identifier, binders)


class NullBinder(Binder):
    def __repr__(self):
        return "_"


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
