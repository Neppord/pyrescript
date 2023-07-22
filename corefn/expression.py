class Expression(object):
    def eval(self, interpreter, frame):
        raise NotImplementedError("%s have yet to implement interpret" % type(self))

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

        arguments_ = []

        for arg in arguments:
            from corefn.var import LocalVar, ExternalVar
            if isinstance(arg, LocalVar) or isinstance(arg, ExternalVar):
                arguments_.append(arg.__repr__())
            else:
                arguments_.append("(%s)" % arg.__repr__())

        arguments_repr = " ".join(arguments_)
        current_repr = current.__repr__()
        on_oneline = "%s %s" % (current_repr, arguments_repr)
        if len(on_oneline) > 79:
            return "%s%s" % (current_repr, "".join(["\n    %s" % a for a in arguments_]))
        else:
            return on_oneline

    def eval(self, interpreter, frame):
        from corefn.abs import AbsInterface
        abstraction = self.abstraction.eval(interpreter, frame)

        if isinstance(abstraction, AbsInterface):
            argument = self.argument.eval(interpreter, frame)
            result = abstraction.call_abs(interpreter, argument)
            return result
        else:
            raise ValueError("%s is not callable" % abstraction.__repr__())


class Accessor(Expression):
    def __init__(self, expression, field_name):
        self.expression = expression
        assert isinstance(field_name, str)
        self.field_name = field_name

    def eval(self, interpreter, frame):
        from corefn.literals import Record
        record = self.expression.eval(interpreter, frame)
        if isinstance(record, Record):
            return record.obj[self.field_name]
        else:
            raise ValueError("%s was not a record" % record.__repr__())

    def __repr__(self):
        return "%s.%s" % (self.expression.__repr__(), self.field_name)


class Let(Expression):

    def __init__(self, binds, expression):
        self.binds = binds
        self.expression = expression

    def eval(self, interpreter, frame):
        new_frame = {}
        new_frame.update(frame)
        # TODO: eval all of the bindings exactly once
        for k, v in self.binds.items():
            new_frame[k] = v
        for k in new_frame.keys():
            new_frame[k] = new_frame[k].eval(interpreter, new_frame)
        return self.expression.eval(interpreter, new_frame)

    def __repr__(self):
        binds = '  ' + '\n  '.join([k + " = " + b.__repr__() for k, b in self.binds.items()])
        expression = self.expression.__repr__()
        return "let\n" + binds + "\nin " + expression
