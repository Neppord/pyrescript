class Expression(object):
    def __repr__(self):
        raise NotImplementedError("%r" % type(self))


class App(Expression):
    def __init__(self, abstraction, argument):
        self.argument = argument
        self.abstraction = abstraction

class Accessor(Expression):
    def __init__(self, expression, field_name):
        self.expression = expression
        assert isinstance(field_name, str)
        self.field_name = field_name

    def __repr__(self):
        return "%s.%s" % (self.expression.__repr__(), self.field_name)


class Let(Expression):

    def __init__(self, binds, expression):
        self.binds = binds
        self.expression = expression

    def __repr__(self):
        binds = '  ' + '\n  '.join([k + " = " + b.__repr__() for k, b in self.binds.items()])
        expression = self.expression.__repr__()
        return "let\n" + binds + "\nin " + expression
