from purescript.corefn.binders import Match
from purescript.corefn.expression import Expression
from purescript.corefn.literals import Boolean


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

    def eval(self, interpreter, frame):
        to_matchs = []
        for e in self.expressions:
            to_matchs.append(e.fix_eval(interpreter, frame))

        for alternative in self.alternatives:
            if isinstance(alternative, Alternative):
                binders = alternative.binders
                assert len(to_matchs) == len(binders)
                next_frame = {}
                for i, binder in enumerate(binders):
                    match = binder.eval(interpreter, to_matchs[i], frame)
                    if isinstance(match, Match):
                        next_frame.update(frame)
                        next_frame.update(match.frame)
                    else:
                        break
                else:
                    return alternative.expression.fix_eval(interpreter, next_frame)
            elif isinstance(alternative, GuardedAlternative):
                binders = alternative.binders
                assert len(to_matchs) == len(binders)
                next_frame = {}
                for i, binder in enumerate(binders):
                    match = binder.eval(interpreter, to_matchs[i], frame)
                    if isinstance(match, Match):
                        next_frame.update(frame)
                        next_frame.update(match.frame)
                    else:
                        break
                else:
                    guard_frame = {}
                    guard_frame.update(frame)
                    guard_frame.update(next_frame)
                    guarded_expressions = alternative.guarded_expressions
                    for guard, expression in guarded_expressions:
                        assert isinstance(guard, Expression)
                        result = guard.fix_eval(interpreter, guard_frame)
                        assert isinstance(result, Boolean)
                        if result.value:
                            return expression
            else:
                raise NotImplementedError("do not support %r yet" % alternative)
        raise NotImplementedError

    def __repr__(self):
        expressions = ", ".join([e.__repr__() for e in self.expressions])
        alternatives = "\n".join([a.__repr__() for a in self.alternatives])
        indented_alternatives = "    " + "\n    ".join(alternatives.split("\n"))
        return "case %s of\n%s" % (expressions, indented_alternatives)
