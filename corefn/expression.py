


class Expression(object):
    def interpret(self, interpreter, frame):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class App(Expression):
    def __init__(self, abstraction, argument):
        self.argument = argument
        self.abstraction = abstraction

    def __repr__(self):
        arguments = []
        current = self
        while isinstance(current, App):
            arguments.append(current.argument)
            current = current.abstraction
        arguments.reverse()
        def repr_arg(arg):
            from corefn.var import LocalVar, ExternalVar
            if isinstance(arg, LocalVar) or isinstance(arg, ExternalVar):
                return arg.__repr__()
            else:
                return "(%s)" % arg.__repr__()

        arguments_ = [repr_arg(a) for a in arguments]
        arguments_repr = " ".join(arguments_)
        current_repr = current.__repr__()
        on_oneline = "%s %s" % (current_repr, arguments_repr)
        if len(on_oneline) > 79:
            return "%s%s" % (current_repr, "".join(["\n    %s" % a for a in arguments_]))
        else:
            return on_oneline

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
        body = self.body.__repr__()
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
        body_repr = self.abs.body.__repr__()
        if self.frame:
            frame_repr = "; ".join([k + " = " + v.__repr__() for k, v in self.frame.items()])
            return "\\" + self.abs.argument + " -> let " + frame_repr + " in " + body_repr
        else:
            return "\\" + self.abs.argument + " -> " + body_repr


class Accessor(Expression):
    def __init__(self, expression, fieldName):
        self.expression = expression
        self.fieldName = fieldName

    def interpret(self, interpreter, frame):
        return interpreter.accessor(self.expression, self.fieldName, frame)

    def __repr__(self):
        return "<Accessor>"


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
        binds = '  ' + '\n  '.join([k + " = " + b.__repr__() for k, b in self.binds.items()])
        expression = self.expression.__repr__()
        return "let\n" + binds + "\nin " + expression
