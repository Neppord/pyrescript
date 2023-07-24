import importlib
import os
import sys

from corefn.abs import NotImplementedYet
from corefn.expression import Expression
from prim import prim


def load_python_foreign(module_name):
    cwd = os.getcwd()
    src = os.path.join(cwd, "src")
    sys.path.append(src)
    try:
        python_module = importlib.import_module(module_name)
        if os.path.commonprefix([src, python_module.__file__]) != src:
            reload(python_module)
        return ForeignModule(module_name, python_module.exports)
    except:
        return interpret_foreign(module_name)
    finally:
        sys.path.remove(src)


def interpret_foreign(module_name):
    from foreign import foreign
    if module_name in foreign:
        return ForeignModule(module_name, foreign[module_name])
    else:
        return NotImplementedYet("Could not find foreign module %s" % (module_name))


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


class ModuleInterface:
    def declarations(self):
        raise NotImplementedError()


class Module(ModuleInterface):
    def __init__(self, imports, declarations):
        self.imports = imports
        self.declarations = declarations

    def decl(self, name):
        return self.declarations[name]

    def declarations(self):
        return self.declarations

    def has_decl(self, name):
        return name in self.declarations

    def preload_imports(self, interpreter):
        for name in self.imports:
            if name not in interpreter.loaded_modules and name not in prim:
                interpreter.get_or_load_module(name)

    def __repr__(self):
        return "\n".join([decl.__repr__() for decl in self.declarations.values()])


class ForeignModule(ModuleInterface):
    def __init__(self, name, exports):
        self.name = name
        self.exports = exports

    def decl(self, name):
        return Declaration(name, self.exports[name])

    def declarations(self):
        declarations = {}
        for name, export in self.exports.items():
            declarations[name] = Declaration(name, export)
        return declarations

    def has_decl(self, name):
        return name in self.exports

    def preload_imports(self, interpreter):
        pass

    def __repr__(self):
        return "\n".join([Declaration(k, expr).__repr__() for k, expr in self.exports])
