from corefn import interpret_foreign
from corefn.expression import Expression
from corefn.literals import Object, String, Effect
from prim import prim
from corefn.parsing import load_module, expression_


class Interpreter(object):
    def __init__(self, _load_module):
        self.__load_module = _load_module
        self.loaded_modules = {}

    def get_or_load_module(self, module):
        if not module in self.loaded_modules:
            self.loaded_modules[module] = self.__load_module(module)
        return self.loaded_modules[module]

    def run_main(self, module):
        """
        :type module: Module
        """
        main = module.decl("main").expression.eval(self, {})
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
                return self.expression(decl.expression, {})
            else:
                foreign = interpret_foreign(module_name, identifier)
                assert isinstance(foreign, Expression)
                return foreign

    def accessor(self, expression, field_name, frame):
        record = expression.eval(interpreter, frame)
        assert isinstance(record, Expression)
        return record[field_name]


if __name__ == '__main__':
    module_name_argument, = sys.argv[1:1] or ["Main"]
    Interpreter(load_module).run_main(load_module(module_name_argument))
