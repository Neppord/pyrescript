import json
import sys

from foreign import foreign
from rjson import loads


def load_module(module_name):
    """
    :type module_name: list
    """
    file_name = "output/" + ".".join(module_name) + "/corefn.json"
    with open(file_name) as json_file:
        s = json_file.read()
    data = loads(s)
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


prim = {
    ('Prim',): {
        'undefined': "undefined"
    }
}



def interpret_foreign(module_name, identifier):
    if tuple(module_name) in foreign and identifier in foreign[tuple(module_name)]:
        return foreign[tuple(module_name)][identifier]
    else:
        raise NotImplementedError


class Expression:

    def interpret(self, interpreter, frame):
        raise NotImplementedError


class App(Expression):
    def __init__(self, abstraction, argument):
        self.argument = argument
        self.abstraction = abstraction

    def __repr__(self):
        f = repr(self.abstraction)
        a = repr(self.argument)
        return "{f} ({a})" % {f: f, a: a}

    def interpret(self, interpreter, frame):
        function = interpreter.expression(self.abstraction, frame)
        argument = interpreter.expression(self.argument, frame)
        return function(argument)


class Abs(Expression):
    def __init__(self, argument, body):
        self.argument = argument
        self.body = body

    def interpret(self, interpreter, frame):
        return AbsWithFrame(interpreter, self, frame)

    def __repr__(self):
        argument = self.argument
        body = repr(self.body)
        return "\\{argument} -> {body} " % {argument: argument, body: body}


class AbsWithFrame:

    def __init__(self, interpreter, abs, frame):
        self.interpreter = interpreter
        self.abs = abs
        self.frame = frame

    def __call__(self, x, **kwargs):
        new_frame = {}
        new_frame.update(self.frame)
        new_frame[self.abs.argument] = x
        return self.interpreter.expression(self.abs.body, new_frame)

    def __repr__(self):
        body_repr = repr(self.abs.body)
        if self.frame:
            frame_repr = "; ".join(k + " = " + repr(v) for k, v in self.frame.items())
            return "\\" + self.abs.argument + " -> let " + frame_repr + " in " + body_repr
        else:
            return "\\" + self.abs.argument + " -> " +body_repr


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        literal_type = self.value["literalType"]
        if literal_type in ["StringLiteral", "BooleanLiteral", "IntLiteral"]:
            return repr(self.value["value"])
        elif literal_type == "ObjectLiteral":
            return repr({k: repr(json_to_expression(v)) for k, v in self.value["value"]})
        raise NotImplementedError

    def interpret(self, interpreter, frame):
        return interpreter.literal(self.value, frame)


class Var(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if 'moduleName' in self.value:
            return '.'.join(self.value['moduleName']) + "." + self.value['identifier']
        else:
            return self.value['identifier']

    def interpret(self, interpreter, frame):
        return interpreter.var(self.value, frame)


class Case(Expression):
    def __init__(self, case_expressions, case_alternatives):
        self.caseExpressions = case_expressions
        self.caseAlternatives = case_alternatives

    def interpret(self, interpreter, frame):
        return interpreter.case(self.caseExpressions, self.caseAlternatives, frame)


class Accessor(Expression):
    def __init__(self, expression, fieldName):
        self.expression = expression
        self.fieldName = fieldName

    def interpret(self, interpreter, frame):
        return interpreter.accessor(self.expression, self.fieldName, frame)


class Let(Expression):
    def __init__(self, binds, expression):
        self.binds = binds
        self.expression = expression

    def interpret(self, interpreter, frame):
        return interpreter.let(self.binds, self.expression, frame)

    def __repr__(self):
        binds = '  ' + '\n  '.join(repr(b) for b in self.binds)
        expression = repr(self.expression)
        return "let\n{binds}\nin {expression}" % {binds: binds, expression: expression}


def json_to_expression(expression):
    type_ = expression["type"]
    if type_ == "App":
        return App(json_to_expression(expression["abstraction"]), json_to_expression(expression["argument"]))
    elif type_ == "Abs":
        return Abs(expression["argument"], json_to_expression(expression["body"]))
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
        name = self.name
        expression = self.expression
        return "{name} = {expression}" % {name: name, expression: expression}

    def get_declarations(self):
        return self


class RecDeclaration:
    def __init__(self, binds):
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

    def decl(self, name):
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

    def declaration(self, decl):
        return self.expression(decl.expression, {})

    def literal(self, literal, frame):
        literal_type = literal["literalType"]
        if literal_type in ["StringLiteral", "BooleanLiteral", "IntLiteral"]:
            return literal["value"]
        elif literal_type == "ObjectLiteral":
            return {k: self.expression(json_to_expression(v), frame) for k, v in literal["value"]}
        raise NotImplementedError

    def expression(self, expression, frame):
        return expression.interpret(self, frame)

    def case(self, expressions, alternatives, frame):
        expression, = expressions
        to_match = json_to_expression(expression)
        for alternative in alternatives:
            alternative_expression = json_to_expression(alternative["expression"])
            binder, = alternative["binders"]
            result, new_frame = self.binder(binder, to_match, frame)
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
