import importlib
import os
import sys

from purescript.corefn.expression import Expression
from purescript.prim import prim


def load_python_foreign(module_name):
    cwd = os.getcwd()
    src = os.path.join(cwd, "src")
    sys.path.append(src)
    try:
        python_module = importlib.import_module(module_name)
        if os.path.commonprefix([src, python_module.__file__]) != src:
            reload(python_module)
        return python_module.exports
    except:
        return interpret_foreign(module_name)
    finally:
        sys.path.remove(src)


def interpret_foreign(module_name):
    from purescript.foreign import foreign
    if module_name in foreign:
        return foreign[module_name]
    else:
        raise NotImplementedError("Could not find foreign module %s" % (module_name))


class Declaration(object):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        name = self.name
        expression = self.expression
        return name + " = " + expression.__repr__()

    def get_declarations(self):
        return self


class Module(object):
    def __init__(self, imports, declarations):
        self.imports = imports
        self.__declarations = declarations

    def declarations(self):
        return self.__declarations

    def has_decl(self, name):
        return name in self.declarations

    def preload_imports(self, interpreter):
        for name in self.imports:
            if name not in interpreter.loaded_modules and name not in prim:
                interpreter.get_or_load_module(name)

    def __repr__(self):
        return "\n".join([decl.__repr__() for decl in self.declarations.values()])
