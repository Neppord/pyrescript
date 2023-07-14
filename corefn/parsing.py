from corefn import Declaration, Module
from corefn.expression import App, Abs, Accessor, Let
from corefn.binders import VarBinder, LiteralBinder, ConstructorBinder, NullBinder, NamedBinder
from corefn.case import Alternative, GuardedAlternative, Case
from corefn.var import LocalVar, ExternalVar
from corefn.literals import ObjectLiteral, ArrayLiteral, ValueLiteral
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
                expression = expression_(bind['expression'])
                declarations[identifier] = Declaration(identifier, expression)
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
