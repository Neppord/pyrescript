from foreign import foreign
from rjson import raw_loads
from rpython.rlib.parsing.tree import Symbol


def load_module(module_name):
    """
    :type module_name: list
    """
    file_name = "output/" + ".".join(module_name) + "/corefn.json"
    with open(file_name) as json_file:
        s = json_file.read()
    module = raw_loads(s)
    for child in module.children:
        if str_(child.children[0]) == 'decls':
            decls = child.children[1]
            break
    else:
        raise "could not find declarations in module for %r" % (module_name,)
    declarations = {}
    for child in decls.children:
        decl = dict(iter_object(child))
        bind_type = str_(decl["bindType"])
        if bind_type == "NonRec":
            name = str_(decl["identifier"])
            expression = expression_(decl["expression"])
            declarations[str_(decl["identifier"])] = Declaration(name, expression)
        elif bind_type == "Rec":
            for child in decl["binds"].children:
                bind = dict(iter_object(child))
                identifier = str_(bind['identifier'])
                declarations[identifier] = Declaration(
                    identifier,
                    expression_(bind['expression'])
                )
        else:
            raise NotImplementedError()
    return Module(declarations)


def iter_object(object):
    """

    :type object: rpython.rlib.parsing.tree.Nonterminal
    """
    return ((str_(c.children[0]), c.children[1]) for c in object.children)


def str_(node):
    """

    :type node: rpython.rlib.parsing.tree.Symbol
    """
    return node.token.source.strip('"')


def expression_(node):
    """

    :type node: rpython.rlib.parsing.tree.Nonterminal
    """
    expr = dict(iter_object(node))
    type_ = str_(expr["type"])
    if type_ == "App":
        return App(expression_(expr["abstraction"]), expression_(expr["argument"]))
    elif type_ == "Abs":
        return Abs(str_(expr["argument"]), expression_(expr["body"]))
    elif type_ == "Literal":
        value = dict(iter_object(expr["value"]))
        literal_type = str_(value["literalType"])
        value_ = value["value"]  # type: Symbol
        if literal_type == "ObjectLiteral":
            obj = {k: expression_(v) for k, v in iter_object(value_)}
            return ObjectLiteral(obj)
        elif literal_type == "ArrayLiteral":
            array = [expression_(v) for v in value_.children]
            return ArrayLiteral(array)
        else:
            symbol = value_.symbol
            if symbol == "STRING":
                return ValueLiteral(str_(value_))
            elif symbol == "INTEGER":
                return ValueLiteral(int(value_.token.source))
            elif symbol == "FLOAT":
                return ValueLiteral(float(value_.token.source))
            elif "true" in symbol:
                return ValueLiteral(True)
            elif "false" in symbol:
                return ValueLiteral(False)
            elif "null" in symbol:
                return ValueLiteral(None)
            else:
                msg = "not implemented literal for symbol %r" % (symbol,)
                raise NotImplementedError(msg)
    elif type_ == "Var":
        value = dict(iter_object(expr["value"]))
        identifier = str_(value["identifier"])
        if "moduleName" in value:
            module_name = tuple(str_(name) for name in value["moduleName"].children)
            return ExternalVar(module_name, identifier)
        else:
            return LocalVar(identifier)
    elif type_ == "Case":
        case_expressions_ = [expression_(c) for c in expr["caseExpressions"].children]
        case_alternatives_ = [alternative_(c) for c in expr["caseAlternatives"].children]
        return Case(case_expressions_, case_alternatives_)
    elif type_ == "Accessor":
        return Accessor(expression_(expr["expression"]), str_(expr["fieldName"]))
    elif type_ == "Let":
        binds = {}
        for c in expr["binds"].children:
            bind = dict(iter_object(c))
            bind_type = str_(bind["bindType"])
            if bind_type == "NonRec":
                identifier = str_(bind['identifier'])
                expression = expression_(bind["expression"])
                binds[identifier] = expression
            elif bind_type == "Rec":
                for child in bind["binds"].children:
                    rec = dict(iter_object(child))
                    identifier = str_(rec['identifier'])
                    binds[identifier] = expression_(rec['expression'])
            else:
                raise NotImplementedError("dont know how to handle %r" % bind_type)
        return Let(binds, expression_(expr["expression"]))
    else:
        raise NotImplementedError


def alternative_(node):
    alternative = dict(iter_object(node))
    is_guarded = str_(alternative["isGuarded"])
    binders = ([binder_(c) for c in alternative["binders"].children])
    if is_guarded == "true":
        guarded_expressions = []
        for c in alternative["expressions"].children:
            child = dict(iter_object(c))
            expression = expression_(child["expression"])
            guard = expression_(child["guard"])
            guarded_expressions.append((guard, expression))
        return GuardedAlternative(binders, guarded_expressions)
    else:
        expression = expression_(alternative["expression"])
        return Alternative(binders, expression)


class VarBinder(object):
    def __init__(self, name):
        self.name = name

    def interpret(self, interpreter, to_match, frame):
        return True, {self.name: to_match}


class LiteralBinder(object):
    def __init__(self, value):
        self.value = value

    def interpret(self, interpreter, to_match, frame):
        return self.value == interpreter.expression(to_match, frame), {}


class ConstructorBinder(object):
    def __init__(self, binders):
        self.binders = binders

    def interpret(self, interpreter, to_match, frame):
        frames = [b.interpret(interpreter, to_match, frame) for b in self.binders]
        new_frame = {}
        for r, f in frames:
            if r:
                new_frame.update(f)
            else:
                return False, {}
        return True, new_frame


class NullBinder(object):
    def interpret(self, interpreter, to_match, frame):
        return True, {}


class ArrayBinder(object):
    pass


class NamedBinder(object):
    def __init__(self, name, binder):
        self.name = name
        self.binder = binder


def binder_(node):
    binder = dict(iter_object(node))
    type_ = str_(binder["binderType"])
    if type_ == "VarBinder":
        return VarBinder(str_(binder["identifier"]))
    elif type_ == "LiteralBinder":
        literal = dict(iter_object(binder["literal"]))
        type_ = str_(literal["literalType"])
        value_ = literal["value"]
        symbol = value_.symbol
        if type_ == "ObjectLiteral":
            value = {k: binder_(v) for k, v in iter_object(literal['value'])}
        elif symbol == "STRING":
            value = (str_(value_))
        elif symbol == "INTEGER":
            value = (int(value_.token.source))
        elif symbol == "FLOAT":
            value = (float(value_.token.source))
        elif "true" in symbol:
            value = (True)
        elif "false" in symbol:
            value = (False)
        elif "null" in symbol:
            value = (None)
        elif "array" in symbol:
            value = [binder_(b) for b in value_.children]
        else:
            msg = "not implemented literal for symbol %r" % (symbol,)
            raise NotImplementedError(msg)
        return LiteralBinder(value)
    elif type_ == "ConstructorBinder":
        constructor_binder = binder
        return ConstructorBinder([binder_(b) for b in constructor_binder["binders"].children])
    elif type_ == "NullBinder":
        return NullBinder()
    elif type_ == "NamedBinder":
        name = str_(binder["identifier"])
        return NamedBinder(name, binder_(binder["binder"]))
    raise NotImplementedError()


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
        return repr(self.abstraction) + " (" + repr(self.argument) + ")"

    def interpret(self, interpreter, frame):
        function = self.abstraction.interpret(interpreter, frame)
        while isinstance(function, Expression):
            function = function.interpret(interpreter, frame)
        argument = self.argument.interpret(interpreter, frame)
        while isinstance(argument, Expression):
            argument = argument.interpret(interpreter, frame)
        return function(argument)


class Alternative(object):
    def __init__(self, binders, expression):
        self.binders = binders
        self.expression = expression


class GuardedAlternative(object):
    def __init__(self, binders, guarded_expressions):
        self.binders = binders
        self.guarded_expressions = guarded_expressions


class Abs(Expression):
    def __init__(self, argument, body):
        self.argument = argument
        self.body = body

    def interpret(self, interpreter, frame):
        return AbsWithFrame(interpreter, self, frame)

    def __repr__(self):
        argument = self.argument
        body = repr(self.body)
        return "\\" + argument + " -> " + body


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
            return "\\" + self.abs.argument + " -> " + body_repr


class ObjectLiteral(Expression):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return repr(self.obj)

    def interpret(self, interpreter, frame):
        return self.obj


class ArrayLiteral(Expression):
    def __init__(self, array):
        self.array = array

    def __repr__(self):
        return repr(self.array)

    def interpret(self, interpreter, frame):
        return self.array


class ValueLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def interpret(self, interpreter, frame):
        return self.value


class LocalVar(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def interpret(self, interpreter, frame):
        return frame[self.name]


class ExternalVar(Expression):
    def __init__(self, module_name, name):
        self.module_name = module_name
        self.name = name

    def __repr__(self):
        return '.'.join(self.module_name) + "." + self.name

    def interpret(self, interpreter, frame):
        return interpreter.load_decl(self.module_name, self.name)


class Case(Expression):
    def __init__(self, expressions, alternatives):
        self.expressions = expressions
        self.alternatives = alternatives

    def interpret(self, interpreter, frame):
        to_match, = self.expressions
        for alternative in self.alternatives:
            if isinstance(alternative, Alternative):
                binder, = alternative.binders
                result, new_frame = binder.interpret(interpreter, to_match, frame)
                if result:
                    next_frame = {}
                    next_frame.update(frame)
                    next_frame.update(new_frame)
                    return interpreter.expression(alternative.expression, next_frame)
            else:
                raise NotImplementedError("do not support %r yet" % alternative)
        raise NotImplementedError


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
        new_frame = {}
        new_frame.update(frame)
        new_frame.update({k: v.interpret(interpreter, frame) for k, v in self.binds.items()})
        return interpreter.expression(self.expression, new_frame)

    def __repr__(self):
        binds = '  ' + '\n  '.join(repr(b) for b in self.binds)
        expression = repr(self.expression)
        return "let\n%(binds)\nin %(expression)" % {binds: binds, expression: expression}


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
