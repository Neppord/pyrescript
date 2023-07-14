class Expression(object):
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
