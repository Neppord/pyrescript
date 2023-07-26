from purescript.corefn.literals import Boolean


class Binder(object):
    def __repr__(self):
        raise NotImplementedError()

    def emit_bytecode(self, emitter):
        raise NotImplementedError()


class VarBinder(Binder):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def emit_bytecode(self, emitter):
        emitter.bytecode.emit_store(self.name)
        return []


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

    def emit_bytecode(self, emitter):
        return [emitter.bytecode.emit_guard_value(Boolean(self.value))]


class RecordBinder(Binder):
    def __init__(self, record):
        self.record = record

    def __repr__(self):
        return "{" + ", ".join([
            "%s:%s" % (k, v.__repr__())
            for k, v in self.record.items()
        ]) + "}"


class ArrayLiteralBinder(Binder):
    def __init__(self, binders):
        self.binders = binders

    def __repr__(self):
        items = ", ".join([b.__repr__() for b in self.binders])
        return "[%s]" % items

    def emit_bytecode(self, emitter):
        go_to_nexts = []
        for binder in self.binders:
            go_to_nexts.extend(binder.emit_bytecode(emitter))
        return go_to_nexts


class ConstructorBinder(Binder):
    def __init__(self, module_name, identifier, binders):
        self.module_name = module_name
        self.identifier = identifier
        self.binders = binders

    def __repr__(self):
        binders = " ".join([b.__repr__() for b in self.binders])
        return "%s.%s %s" % (self.module_name, self.identifier, binders)

    def emit_bytecode(self, emitter):
        go_to_nexts = []
        guard = emitter.bytecode.emit_guard_constructor(self.identifier)
        go_to_nexts.append(guard)
        for binder in self.binders:
            go_to_nexts.extend(binder.emit_bytecode(emitter))
        return go_to_nexts


class NewtypeBinder(Binder):
    def __init__(self, module_name, identifier, binders):
        self.module_name = module_name
        self.identifier = identifier
        self.binders = binders

    def __repr__(self):
        binders = " ".join([b.__repr__() for b in self.binders])
        return "%s.%s %s" % (self.module_name, self.identifier, binders)

    def emit_bytecode(self, emitter):
        go_to_nexts = []
        for binder in self.binders:
            go_to_nexts.extend(binder.emit_bytecode(emitter))
        return go_to_nexts


class NullBinder(Binder):
    def __repr__(self):
        return "_"

    def emit_bytecode(self, emitter):
        emitter.bytecode.emit_pop()
        return []


class NamedBinder(Binder):
    def __init__(self, name, binder):
        self.name = name
        self.binder = binder

    def __repr__(self):
        return "%s@%s" % (self.name, self.binder.__repr__())
