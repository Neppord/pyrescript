from purescript.corefn.expression import Expression


class LocalVar(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class ExternalVar(Expression):
    def __init__(self, module_name, name):
        self.module_name = module_name
        self.name = name

    def __repr__(self):
        return self.module_name + "." + self.name
