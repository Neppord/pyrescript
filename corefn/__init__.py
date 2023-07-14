from foreign import foreign


def interpret_foreign(module_name, identifier):
    if tuple(module_name) in foreign and identifier in foreign[tuple(module_name)]:
        return foreign[tuple(module_name)][identifier]
    else:
        raise NotImplementedError


class Declaration(object):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        name = self.name
        expression = self.expression
        return "%(name) = %(expression)" % {name: name, expression: expression}

    def get_declarations(self):
        return self


class Module:
    def __init__(self, declarations):
        self.declarations = declarations

    def decl(self, name):
        return self.declarations[name]

    def has_decl(self, name):
        return name in self.declarations

    def __repr__(self):
        return "\n".join(repr(decl) for decl in self.declarations.values())
