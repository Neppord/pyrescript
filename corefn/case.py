from corefn.expression import Expression


class AlternativeInterface(object):
    def __repr__(self):
        raise NotImplementedError()


class Alternative(AlternativeInterface):
    def __init__(self, binders, expression):
        self.binders = binders
        self.expression = expression

    def __repr__(self):
        binders = ", ".join([b.__repr__() for b in self.binders])
        expression = self.expression.__repr__()
        return "%s -> %s" % (binders, expression)


class GuardedAlternative(AlternativeInterface):
    def __init__(self, binders, guarded_expressions):
        self.binders = binders
        self.guarded_expressions = guarded_expressions

    def __repr__(self):
        binders = ", ".join([b.__repr__() for b in self.binders])
        expressions = "\n    | ".join(["%s -> %s " % (g.__repr__(), e.__repr__()) for g, e in self.guarded_expressions])
        return "%s ->\n   |%s" % (binders, expressions)


class Case(Expression):
    def __init__(self, expressions, alternatives):
        self.expressions = expressions
        self.alternatives = alternatives

    def interpret(self, interpreter, frame):
        to_match, = self.expressions
        for alternative in self.alternatives:
            if isinstance(alternative, Alternative):
                binder, = alternative.binders
                result, new_frame = binder.interpret(interpreter, to_match, frame)
                if result:
                    next_frame = {}
                    next_frame.update(frame)
                    next_frame.update(new_frame)
                    return interpreter.expression(alternative.expression, next_frame)
            else:
                raise NotImplementedError("do not support %r yet" % alternative)
        raise NotImplementedError

    def __repr__(self):
        expressions = ", ".join([e.__repr__() for e in self.expressions])
        alternatives = "\n".join([a.__repr__() for a in self.alternatives])
        indented_alternatives = "    " + "\n    ".join(alternatives.split("\n"))
        return "case %s of\n%s" % (expressions, indented_alternatives)
