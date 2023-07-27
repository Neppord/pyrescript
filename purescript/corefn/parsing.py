from rpython.rlib.parsing.tree import Nonterminal
from rpython.rlib.parsing.tree import Symbol

from purescript.corefn import Declaration, Module
from purescript.corefn.abs import Abs, Constructor
from purescript.corefn.binders import VarBinder, ConstructorBinder, NullBinder, NamedBinder, RecordBinder, \
    StringLiteralBinder, IntBinder, FloatBinder, BoolBinder, ArrayLiteralBinder, CharLiteralBinder, NewtypeBinder
from purescript.corefn.case import Alternative, GuardedAlternative, Case
from purescript.corefn.expression import App, Accessor, Let
from purescript.corefn.value import Array, String, Int, Float, Boolean
from purescript.corefn.literals import RecordLiteral
from purescript.corefn.var import LocalVar, ExternalVar
from purescript.rjson import raw_loads


def load_module(module_name):
    file_name = "output/" + module_name + "/corefn.json"
    with open(file_name) as json_file:
        s = json_file.read()
    module = raw_loads(s)
    module_object = object_(module)
    declarations = []
    for child in module_object["decls"].children:
        decl = object_(child)
        bind_type = str_(decl["bindType"])
        if bind_type == "NonRec":
            identifier = str_(decl["identifier"])
            expression = expression_(decl["expression"])
            declarations.append(Declaration(identifier, expression))
        elif bind_type == "Rec":
            for child in decl["binds"].children:
                bind = object_(child)
                identifier = str_(bind['identifier'])
                expression = expression_(bind['expression'])
                declarations.append(Declaration(identifier, expression))
        else:
            raise NotImplementedError()
    imports = []
    for child in module_object["imports"].children:
        imported_module_name = ".".join([str_(c) for c in object_(child)["moduleName"].children])
        imports.append(imported_module_name)
    return Module(imports, declarations)


def iter_object(node):
    """

    :type node: rpython.rlib.parsing.tree.Nonterminal
    """
    return [(str_(c.children[0]), c.children[1]) for c in node.children]


def object_(node):
    obj = {}
    for k, v in iter_object(node):
        obj[k] = v
    return obj


def str_(node):
    """

    :type node: rpython.rlib.parsing.tree.Symbol
    """
    return node.token.source.strip('"')


def expression_(node):
    """

    :type node: rpython.rlib.parsing.tree.Nonterminal
    """
    expr = object_(node)
    type_ = str_(expr["type"])
    if type_ == "App":
        return App(expression_(expr["abstraction"]), expression_(expr["argument"]))
    elif type_ == "Abs":
        return Abs(str_(expr["argument"]), expression_(expr["body"]))
    elif type_ == "Literal":
        value = object_(expr["value"])
        literal_type = str_(value["literalType"])
        if literal_type == "ObjectLiteral":
            value_ = value["value"]  # type: Nonterminal
            obj = {}
            for k, v in iter_object(value_):
                obj[k] = expression_(v)
            return RecordLiteral(obj)
        elif literal_type == "ArrayLiteral":
            value_ = value["value"]  # type: Nonterminal
            array = [expression_(v) for v in value_.children]
            return Array(array)
        else:
            value_ = value["value"]  # type: Symbol
            symbol = value_.symbol
            if symbol == "STRING":
                return String(str_(value_))
            elif symbol == "INTEGER":
                return Int(int(value_.token.source))
            elif symbol == "FLOAT":
                return Float(float(value_.token.source))
            elif "true" in symbol:
                return Boolean(True)
            elif "false" in symbol:
                return Boolean(False)
            else:
                msg = "not implemented literal for symbol: " + symbol
                raise NotImplementedError(msg)
    elif type_ == "Var":
        value = object_(expr["value"])
        identifier = str_(value["identifier"])
        if "moduleName" in value:
            module_name = ".".join([str_(name) for name in value["moduleName"].children])
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
            bind = object_(c)
            bind_type = str_(bind["bindType"])
            if bind_type == "NonRec":
                identifier = str_(bind['identifier'])
                expression = expression_(bind["expression"])
                binds[identifier] = expression
            elif bind_type == "Rec":
                for child in bind["binds"].children:
                    rec = object_(child)
                    identifier = str_(rec['identifier'])
                    expression = expression_(rec['expression'])
                    binds[identifier] = expression
            else:
                raise NotImplementedError("dont know how to handle: " + bind_type)
        return Let(binds, expression_(expr["expression"]))
    elif type_ == "Constructor":
        name = str_(expr["constructorName"])
        field_names = [str_(c) for c in expr["fieldNames"].children]
        return Constructor(name, field_names)
    else:
        raise NotImplementedError("Cant parse type: " + type_)


def alternative_(node):
    alternative = object_(node)
    is_guarded = str_(alternative["isGuarded"])
    binders = ([binder_(c) for c in alternative["binders"].children])
    if is_guarded == "true":
        guarded_expressions = []
        for c in alternative["expressions"].children:
            child = object_(c)
            expression = expression_(child["expression"])
            guard = expression_(child["guard"])
            guarded_expressions.append((guard, expression))
        return GuardedAlternative(binders, guarded_expressions)
    else:
        expression = expression_(alternative["expression"])
        return Alternative(binders, expression)


def binder_(node):
    binder = object_(node)
    type_ = str_(binder["binderType"])
    if type_ == "VarBinder":
        return VarBinder(str_(binder["identifier"]))
    elif type_ == "LiteralBinder":
        literal = object_(binder["literal"])
        type_ = str_(literal["literalType"])
        value_ = literal["value"]
        symbol = value_.symbol
        if type_ == "ObjectLiteral":
            value = {}
            for k, v in iter_object(literal['value']):
                value[k] = binder_(v)
            return RecordBinder(value)
        elif type_ == "ArrayLiteral":
            return ArrayLiteralBinder( [binder_(b) for b in value_.children])
        elif type_ == "StringLiteral":
            return StringLiteralBinder(str_(value_))
        elif type_ == "CharLiteral":
            return CharLiteralBinder(str_(value_))
        elif type_ == "IntLiteral":
            return IntBinder(int(value_.token.source))
        elif type_ == "NumberLiteral":
            return FloatBinder(float(value_.token.source))
        elif "true" in symbol:
            return BoolBinder(True)
        elif "false" in symbol:
            return BoolBinder(False)
        else:
            msg = "not implemented literal %s with symbol %s " %(type_, symbol)
            raise NotImplementedError(msg)
    elif type_ == "ConstructorBinder":
        annotation = object_(binder["annotation"])
        meta = object_(annotation["meta"])
        meta_type = str_(meta["metaType"])
        constructor_binder = binder
        constructor_name = object_(constructor_binder["constructorName"])
        module_name = ".".join(str_(n) for n in constructor_name["moduleName"].children)
        identifier = str_(constructor_name["identifier"])
        if meta_type == "IsNewtype":
            return NewtypeBinder(module_name, identifier, [binder_(b) for b in constructor_binder["binders"].children])
        else:
            return ConstructorBinder(module_name, identifier, [binder_(b) for b in constructor_binder["binders"].children])
    elif type_ == "NullBinder":
        return NullBinder()
    elif type_ == "NamedBinder":
        name = str_(binder["identifier"])
        return NamedBinder(name, binder_(binder["binder"]))
    raise NotImplementedError()
