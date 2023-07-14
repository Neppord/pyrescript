from corefn.expression import Expression


class Alternative(object):
    def __init__(self, binders, expression):
        self.binders = binders
        self.expression = expression


class GuardedAlternative(object):
    def __init__(self, binders, guarded_expressions):
        self.binders = binders
        self.guarded_expressions = guarded_expressions


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
