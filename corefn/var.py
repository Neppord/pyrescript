from corefn.expression import Expression


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
        return self.module_name + "." + self.name

    def interpret(self, interpreter, frame):
        return interpreter.load_decl(self.module_name, self.name)
