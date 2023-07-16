from corefn.expression import Expression


class LocalVar(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def eval(self, interpreter, frame):
        value = frame[self.name]
        assert isinstance(value, Expression)
        return value.eval(interpreter, frame)


class ExternalVar(Expression):
    def __init__(self, module_name, name):
        self.module_name = module_name
        self.name = name

    def __repr__(self):
        return self.module_name + "." + self.name

    def eval(self, interpreter, frame):
        value = interpreter.load_decl(self.module_name, self.name)
        assert isinstance(value, Expression)
        return value.eval(interpreter, {})
