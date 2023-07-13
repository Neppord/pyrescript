import json
import sys
from functools import partial, wraps
from typing import List, Dict

from foreign.data_array import range_impl
from foreign.data_eq import eq_int_impl
from foreign.data_euclidean_ring import int_mod, int_div, int_degree
from foreign.data_foldable import foldr_array, foldl_array
from foreign.data_semigroup import concat_string
from foreign.data_semiring import int_add, int_mul


def load_module(module_name):
    file_name = "output/" + ".".join(module_name) + "/corefn.json"
    with open(file_name) as json_file:
        data = json.load(json_file)
    children = [data]
    while children:
        current = children.pop()
        if "annotation" in current:
            del current["annotation"]
        for value in current.values():
            if isinstance(value, dict):
                children.append(value)
            elif isinstance(value, list):
                children.extend(v for v in value if isinstance(v, dict))
    return Module(data)


def not_implemented_effect():
    raise NotImplementedError


prim = {
    ('Prim',): {
        'undefined': "undefined"
    }
}


def pure(x):
    return x


def apply(f):
    def apply2(a):
        return f(a)

    return apply2


def run_fn_2(fn):
    return curry(fn, 2)


def curry(fn, n):
    if n == 1:
        return fn
    elif n == 2:
        return wraps(fn)(lambda x: wraps(fn)(lambda y: fn(x, y)))
    elif n == 3:
        return wraps(fn)(lambda x: wraps(fn)(lambda y: wraps(fn)(lambda z: fn(x, y, z))))
    else:
        raise NotImplementedError


def bindE(a, atob):
    return atob(a)


foreign = {
    ('Effect',): {
        'pureE': pure,
        'bindE': curry(bindE, 2)
    },
    ('Effect', 'Console'): {
        'log': print
    },
    ('Data', 'Array'): {
        'rangeImpl': range_impl,
    },
    ('Data', 'Eq'): {
        'eqIntImpl': eq_int_impl,
    },
    ('Data', 'EuclideanRing'): {
        'intDegree': int_degree,
        'intDiv': curry(int_div, 2),
        'intMod': curry(int_mod, 2),
    },
    ('Data', 'Foldable'): {
        'foldrArray': curry(foldr_array, 3),
        'foldlArray': curry(foldl_array, 3),
    },
    ('Data', 'Function', 'Uncurried'): {
        'runFn2': run_fn_2,
    },
    ('Data', 'Semigroup'): {
        'concatString': curry(concat_string, 2)
    },
    ('Data', 'Semiring'): {
        'intAdd': curry(int_add, 2),
        'intMul': curry(int_mul, 2),
    },
    ('Data', 'Show'): {
        'showIntImpl': str
    },
    ('Data', 'Unit'): {
        'unit': None
    },
}


def intMod(a, b):
    abs_b = abs(b)
    return ((a % abs_b) + abs_b) % abs_b


def interpret_foreign(module_name, identifier):
    if tuple(module_name) in foreign and identifier in foreign[tuple(module_name)]:
        return foreign[tuple(module_name)][identifier]
    else:
        raise NotImplementedError


class App:
    def __init__(self, abstraction, argument):
        self.argument = argument
        self.abstraction = abstraction

    def __repr__(self):
        return f"{repr(self.abstraction)} ({repr(self.argument)})"


class Abs:
    def __init__(self, argument, body):
        self.argument = argument
        self.body = json_to_expression(body)


class Literal:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        literal_type = self.value["literalType"]
        if literal_type in ["StringLiteral", "BooleanLiteral", "IntLiteral"]:
            return self.value["value"]
        elif literal_type == "ObjectLiteral":
            return repr({k: repr(json_to_expression(v)) for k, v in self.value["value"]})
        raise NotImplementedError


class Var:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{'.'.join(self.value['moduleName'])}.{self.value['identifier']}"


class Case:
    def __init__(self, caseExpressions, caseAlternatives):
        self.caseExpressions = caseExpressions
        self.caseAlternatives = caseAlternatives


class Accessor:
    def __init__(self, expression, fieldName):
        self.expression = expression
        self.fieldName = fieldName


class Let:
    def __init__(self, binds, expression):
        self.binds = binds
        self.expression = expression


def json_to_expression(expression):
    type_ = expression["type"]
    if type_ == "App":
        return App(json_to_expression(expression["abstraction"]), json_to_expression(expression["argument"]))
    elif type_ == "Abs":
        return Abs(expression["argument"], expression["body"])
    elif type_ == "Literal":
        return Literal(expression["value"])
    elif type_ == "Var":
        return Var(expression["value"])
    elif type_ == "Case":
        return Case(expression["caseExpressions"], expression["caseAlternatives"])
    elif type_ == "Accessor":
        return Accessor(json_to_expression(expression["expression"]), expression["fieldName"])
    elif type_ == "Let":
        return Let(expression["binds"], json_to_expression(expression["expression"]))
    else:
        raise NotImplementedError


class NonRecDeclaration:
    def __init__(self, name, expression):
        self.name = name
        self.expression = json_to_expression(expression)

    def __repr__(self):
        return f"{self.name} = {self.expression}"

    def get_declarations(self):
        return self


class RecDeclaration:
    def __init__(self, binds: List):
        self.binds = [
            NonRecDeclaration(bind['identifier'], bind['expression'])
            for bind in binds
        ]

    def __repr__(self):
        return "\n".join(repr(bind) for bind in self.binds)

    def get_declarations(self):
        return self.binds


class Module:
    def __init__(self, module):
        self.module = module
        self.declarations = [
            NonRecDeclaration(decl['identifier'], decl['expression'])
            if decl['bindType'] == "NonRec" else
            RecDeclaration(decl["binds"])
            for decl in module['decls']
        ]

    def decl(self, name) -> NonRecDeclaration:
        for decl in self.declarations:
            if isinstance(decl, NonRecDeclaration) and decl.name == name:
                return decl
            elif isinstance(decl, RecDeclaration):
                for bind in decl.binds:
                    if bind.name == name:
                        return bind
        raise NotImplementedError

    def has_decl(self, name):
        for decl in self.module["decls"]:
            bind_type = decl["bindType"]
            if bind_type == "NonRec":
                if decl["identifier"] == name:
                    return True
            elif bind_type == "Rec":
                for bind in decl["binds"]:
                    if bind["identifier"] == name:
                        return True
        return False

    def __repr__(self):
        return "\n".join(repr(decl) for decl in self.declarations)


class Interpreter(object):
    def __init__(self, _load_module):
        self.load_module = _load_module

    def run_main(self, module):
        self.declaration(module.decl("main"))

    def run_module_by_name(self, module_name):
        self.run_main(self.load_module(module_name))

    def declaration(self, decl: NonRecDeclaration):
        return self.expression(decl.expression, {})

    def literal(self, literal, frame):
        literal_type = literal["literalType"]
        if literal_type in ["StringLiteral", "BooleanLiteral", "IntLiteral"]:
            return literal["value"]
        elif literal_type == "ObjectLiteral":
            return {k: self.expression(json_to_expression(v), frame) for k, v in literal["value"]}
        raise NotImplementedError

    def expression(self, expression, frame):
        if isinstance(expression, Literal):
            return self.literal(expression.value, frame)
        elif isinstance(expression, Var):
            return self.var(expression.value, frame)
        elif isinstance(expression, Abs):
            def abs(x):
                return self.expression(expression.body, {expression.argument: x} | frame)

            return abs
        elif isinstance(expression, App):
            function = self.expression(expression.abstraction, frame)
            argument = self.expression(expression.argument, frame)
            return function(argument)
        elif isinstance(expression, Case):
            return self.case(expression.caseExpressions, expression.caseAlternatives, frame)
        elif isinstance(expression, Accessor):
            return self.accessor(expression.expression, expression.fieldName, frame)
        elif isinstance(expression, Let):
            return self.let(expression.binds, expression.expression, frame)
        else:
            raise NotImplementedError

    def case(self, expressions, alternatives, frame):
        expression, = expressions
        to_match = json_to_expression(expression)
        for alternative in alternatives:
            alternative_expression = json_to_expression(alternative["expression"])
            binder, = alternative["binders"]
            result, new_frame = self.binder(binder, to_match, frame)
            if result:
                return self.expression(alternative_expression, new_frame | frame)
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

    def load_decl(self, full_name):
        module_name = full_name["moduleName"]
        identifier = full_name["identifier"]
        if tuple(module_name) in prim:
            if identifier in prim[tuple(module_name)]:
                return prim[tuple(module_name)][identifier]
            else:
                raise NotImplementedError
        else:
            module = self.load_module(module_name)
            if module.has_decl(identifier):
                return self.declaration(module.decl(identifier))
            else:
                return interpret_foreign(module_name, identifier)

    def var(self, value, frame):
        if "moduleName" in value:
            return self.load_decl(value)
        else:
            return frame[value["identifier"]]

    def accessor(self, expression, field_name, frame):
        record = self.expression(expression, frame)
        return record[field_name]

    def let(self, binds, expression, frame):
        new_frame = frame
        for bind in binds:
            new_frame |= self.bind(bind, frame)
        return self.expression(expression, new_frame)

    def bind(self, bind, frame):
        if bind["bindType"] == "NonRec":
            return {bind["identifier"]: self.expression(json_to_expression(bind["expression"]), frame)}
        else:
            raise NotImplementedError


if __name__ == '__main__':
    module_name_argument, = sys.argv[1:1] or ["Main"]
    Interpreter(load_module).run_main(load_module(module_name_argument.split(".")))
