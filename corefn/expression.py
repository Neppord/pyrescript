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


class Expression:

    def interpret(self, interpreter, frame):
        raise NotImplementedError


class App(Expression):
    def __init__(self, abstraction, argument):
        self.argument = argument
        self.abstraction = abstraction

    def __repr__(self):
        return repr(self.abstraction) + " (" + repr(self.argument) + ")"

    def interpret(self, interpreter, frame):
        function = self.abstraction.interpret(interpreter, frame)
        while isinstance(function, Expression):
            function = function.interpret(interpreter, frame)
        argument = self.argument.interpret(interpreter, frame)
        while isinstance(argument, Expression):
            argument = argument.interpret(interpreter, frame)
        return function(argument)


class Alternative(object):
    def __init__(self, binders, expression):
        self.binders = binders
        self.expression = expression


class GuardedAlternative(object):
    def __init__(self, binders, guarded_expressions):
        self.binders = binders
        self.guarded_expressions = guarded_expressions


class Abs(Expression):
    def __init__(self, argument, body):
        self.argument = argument
        self.body = body

    def interpret(self, interpreter, frame):
        return AbsWithFrame(interpreter, self, frame)

    def __repr__(self):
        argument = self.argument
        body = repr(self.body)
        return "\\" + argument + " -> " + body


class AbsWithFrame:

    def __init__(self, interpreter, abs, frame):
        self.interpreter = interpreter
        self.abs = abs
        self.frame = frame

    def __call__(self, x, **kwargs):
        new_frame = {}
        new_frame.update(self.frame)
        new_frame[self.abs.argument] = x
        return self.interpreter.expression(self.abs.body, new_frame)

    def __repr__(self):
        body_repr = repr(self.abs.body)
        if self.frame:
            frame_repr = "; ".join(k + " = " + repr(v) for k, v in self.frame.items())
            return "\\" + self.abs.argument + " -> let " + frame_repr + " in " + body_repr
        else:
            return "\\" + self.abs.argument + " -> " + body_repr


class ObjectLiteral(Expression):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return repr(self.obj)

    def interpret(self, interpreter, frame):
        return self.obj


class ArrayLiteral(Expression):
    def __init__(self, array):
        self.array = array

    def __repr__(self):
        return repr(self.array)

    def interpret(self, interpreter, frame):
        return self.array


class ValueLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def interpret(self, interpreter, frame):
        return self.value


class LocalVar(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def interpret(self, interpreter, frame):
        return frame[self.name]


class ExternalVar(Expression):
    def __init__(self, module_name, name):
        self.module_name = module_name
        self.name = name

    def __repr__(self):
        return '.'.join(self.module_name) + "." + self.name

    def interpret(self, interpreter, frame):
        return interpreter.load_decl(self.module_name, self.name)


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


class Accessor(Expression):
    def __init__(self, expression, fieldName):
        self.expression = expression
        self.fieldName = fieldName

    def interpret(self, interpreter, frame):
        return interpreter.accessor(self.expression, self.fieldName, frame)


class Let(Expression):
    def __init__(self, binds, expression):
        self.binds = binds
        self.expression = expression

    def interpret(self, interpreter, frame):
        new_frame = {}
        new_frame.update(frame)
        new_frame.update({k: v.interpret(interpreter, frame) for k, v in self.binds.items()})
        return interpreter.expression(self.expression, new_frame)

    def __repr__(self):
        binds = '  ' + '\n  '.join(repr(b) for b in self.binds)
        expression = repr(self.expression)
        return "let\n%(binds)\nin %(expression)" % {binds: binds, expression: expression}
