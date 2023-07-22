import importlib
import os
import sys

from corefn.abs import NotImplementedYet
from corefn.expression import Expression
from prim import prim


def load_python_foreign(module_name, identifier):
    cwd = os.getcwd()
    src = os.path.join(cwd, "src")
    sys.path.append(src)
    try:
        python_module = importlib.import_module(module_name)
        if os.path.commonprefix([src, python_module.__file__]) != src:
            reload(python_module)
        imported = python_module.__dict__[identifier]
        assert isinstance(imported, Expression)
        return imported
    except:
        from foreign import foreign
        if module_name in foreign and identifier in foreign[module_name]:
            return foreign[module_name][identifier]
        else:
            return NotImplementedYet("Could not find foreign %s.%s" % (module_name, identifier))
    finally:
        sys.path.remove(src)


def interpret_foreign(module_name, identifier):
    from foreign import foreign
    if module_name in foreign and identifier in foreign[module_name]:
        return foreign[module_name][identifier]
    else:
        return NotImplementedYet("Could not find foreign %s.%s" % (module_name, identifier))


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


class Module:
    def __init__(self, imports, declarations):
        self.imports = imports
        self.declarations = declarations

    def decl(self, name):
        return self.declarations[name]

    def has_decl(self, name):
        return name in self.declarations

    def preload_imports(self, interpreter):
        for name in self.imports:
            if name not in interpreter.loaded_modules and name not in prim:
                interpreter.get_or_load_module(name)

    def __repr__(self):
        return "\n".join([decl.__repr__() for decl in self.declarations.values()])
