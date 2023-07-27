from purescript.corefn.expression import Expression
from purescript.corefn.value import Boolean


class AlternativeInterface(object):
    def __repr__(self):
        raise NotImplementedError()

    def emit_alternative_bytecode(self, emitter):
        raise NotImplementedError()


class Alternative(AlternativeInterface):
    def __init__(self, binders, expression):
        self.binders = binders
        self.expression = expression

    def __repr__(self):
        binders = ", ".join([b.__repr__() for b in self.binders])
        expression = self.expression.__repr__()
        return "%s -> %s" % (binders, expression)

    def emit_alternative_bytecode(self, emitter):
        go_to_ends = []
        go_to_nexts = []
        for binder in self.binders:
            go_to_nexts.extend(binder.emit_bytecode(emitter))
        emitter.emit(self.expression)
        go_to_ends.append(emitter.bytecode.emit_jump())
        for go_to_next in go_to_nexts:
            go_to_next.address = len(emitter.bytecode.opcodes)
        return go_to_ends


class GuardedAlternative(AlternativeInterface):
    def __init__(self, binders, guarded_expressions):
        self.binders = binders
        self.guarded_expressions = guarded_expressions

    def __repr__(self):
        binders = ", ".join([b.__repr__() for b in self.binders])
        expressions = "\n    | ".join(["%s -> %s " % (g.__repr__(), e.__repr__()) for g, e in self.guarded_expressions])
        return "%s ->\n   |%s" % (binders, expressions)

    def emit_alternative_bytecode(self, emitter):
        go_to_ends = []
        go_to_nexts = []
        for binder in self.binders:
            go_to_nexts.extend(binder.emit_bytecode(emitter))
        for guard, expression in self.guarded_expressions:
            emitter.emit(guard)
            goto_next_guard = emitter.bytecode.emit_guard_value(Boolean(True))
            emitter.emit(expression)
            go_to_ends.append(emitter.bytecode.emit_jump())
            goto_next_guard.address = len(emitter.bytecode.opcodes)
        go_to_ends.append(emitter.bytecode.emit_jump())
        for go_to_next in go_to_nexts:
            go_to_next.address = len(emitter.bytecode.opcodes)
        return go_to_ends


class Case(Expression):
    def __init__(self, expressions, alternatives):
        self.expressions = expressions
        self.alternatives = alternatives

    def __repr__(self):
        expressions = ", ".join([e.__repr__() for e in self.expressions])
        alternatives = "\n".join([a.__repr__() for a in self.alternatives])
        indented_alternatives = "    " + "\n    ".join(alternatives.split("\n"))
        return "case %s of\n%s" % (expressions, indented_alternatives)
