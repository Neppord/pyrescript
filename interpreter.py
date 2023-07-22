from corefn.expression import Expression
from corefn.literals import Effect
from prim import prim


class Interpreter(object):
    def __init__(self, _load_foreign, _load_module):
        self.__load_foreign = _load_foreign
        self.__load_module = _load_module
        self.loaded_modules = {}
        self.loaded_foreign_modules = {}

    def get_or_load_module(self, module):
        if module not in self.loaded_modules:
            self.loaded_modules[module] = self.__load_module(module)
        return self.loaded_modules[module]

    def get_or_load_foreign_module(self, module):
        if module not in self.loaded_foreign_modules:
            self.loaded_foreign_modules[module] = self.__load_foreign(module)
        return self.loaded_foreign_modules[module]

    def run_main(self, module):
        """
        :type module: Module
        """
        decl = module.decl("main")  # type: Expression
        main = decl.expression.eval(self, {})
        assert isinstance(main, Effect)
        main.run_effect(self)

    def run_module_by_name(self, module_name):
        self.run_main(self.get_or_load_module(module_name))

    def expression(self, expression, frame):
        return expression.eval(self, frame)

    def load_decl(self, module_name, identifier):
        if module_name in prim:
            if identifier in prim[module_name]:
                return prim[module_name][identifier]
            else:
                raise NotImplementedError
        else:
            module = self.get_or_load_module(module_name)
            if module.has_decl(identifier):
                decl = module.decl(identifier)
                return decl.expression.eval(self, {})
            else:
                module = self.get_or_load_foreign_module(module_name)
                decl = module.decl(identifier)
                return decl.expression.eval(self, {})

