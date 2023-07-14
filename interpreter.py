from corefn import interpret_foreign
from corefn.expression import Expression
from prim import prim
from corefn.parsing import load_module, expression_


class Interpreter(object):
    def __init__(self, _load_module):
        self.__load_module = _load_module
        self.loaded_modules = {}

    def get_or_load_module(self, module):
        module = tuple(module)
        if not module in self.loaded_modules:
            self.loaded_modules[module] = self.__load_module(module)
        return self.loaded_modules[module]

    def run_main(self, module):
        """
        :type module: Module
        """
        self.declaration(module.decl("main"))

    def run_module_by_name(self, module_name):
        self.run_main(self.get_or_load_module(module_name))

    def declaration(self, decl):
        return self.expression(decl.expression, {})

    def expression(self, expression, frame):
        return expression.interpret(self, frame)

    def case(self, expressions, alternatives, frame):
        expression, = expressions
        to_match = expression_(expression)
        for alternative in alternatives:
            alternative_expression = expression_(alternative["expression"])
            binder, = alternative["binders"]
            result, new_frame = binder.interpret(self, to_match, frame)
            if result:
                next_frame = {}
                next_frame.update(frame)
                next_frame.update(new_frame)
                return self.expression(alternative_expression, next_frame)
        raise NotImplementedError

    def binder(self, binder, to_match, frame):
        type_ = binder["binderType"]
        if type_ == "VarBinder":
            raise NotImplementedError
        elif type_ == "LiteralBinder":
            return binder["literal"]["value"] == self.expression(to_match, frame), {}
        elif type_ == "ConstructorBinder":
            constructor_binder = binder
            binder, = constructor_binder["binders"]
            v = self.expression(to_match, frame)
            return True, {binder["identifier"]: v}
        elif type_ == "NullBinder":
            return True, {}
        raise NotImplementedError

    def load_decl(self, module_name, identifier):
        if tuple(module_name) in prim:
            if identifier in prim[tuple(module_name)]:
                return prim[tuple(module_name)][identifier]
            else:
                raise NotImplementedError
        else:
            module = self.get_or_load_module(module_name)
            if module.has_decl(identifier):
                return self.declaration(module.decl(identifier))
            else:
                return interpret_foreign(module_name, identifier)

    def accessor(self, expression, field_name, frame):
        record = expression.interpret(self, frame)
        while isinstance(record, Expression):
            record = record.interpret(self, frame)
        while isinstance(field_name, Expression):
            field_name = field_name.interpret(self, frame)
        return record[field_name]

    def let(self, binds, expression, frame):
        new_frame = {}
        new_frame.update(frame)
        for bind in binds:
            new_frame.update(self.bind(bind, frame))
        return self.expression(expression, new_frame)

    def bind(self, bind, frame):
        if bind["bindType"] == "NonRec":
            return {bind["identifier"]: self.expression(json_to_expression(bind["expression"]), frame)}
        else:
            raise NotImplementedError


if __name__ == '__main__':
    module_name_argument, = sys.argv[1:1] or ["Main"]
    Interpreter(load_module).run_main(load_module(module_name_argument.split(".")))
