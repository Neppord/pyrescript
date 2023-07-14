from rpython.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from rpython.rlib.parsing.tree import RPythonVisitor

EBNF = r'''
IGNORE : " |\n|\r|\t" ;
value : <object> | <array> | <STRING> | <INTEGER> | <FLOAT> | <"true"> | <"false"> | <"null"> ;
key_value_pair: STRING  [":"] value ;
object : ["{"] ["}"] | ["{"] (key_value_pair [","])* key_value_pair ["}"] ;
array: ["["] ["]"] | ["["] (value [","])* value ["]"] ;
STRING: "\"[^\"]*\"";
INTEGER : "\d|[1-9]|\d+|-\d|-[1-9]|\d+" ;
FLOAT: "(\d|[1-9]|\d+|-\d|-[1-9]|\d+)(\.\d+)?([Ee][+-]?\d+)?";
'''

regexes, rules, _to_ast = parse_ebnf(EBNF)
parser = make_parse_function(regexes, rules, eof=True)
to_ast = _to_ast()


class Visitor(RPythonVisitor):
    def visit_object(self, node):
        ret = {}
        for key_value_pair in node.children:
            key, value = self.dispatch(key_value_pair)
            ret[key] = value
        return ret
    def visit_array(self, node):
        return [self.dispatch(c) for c in node.children]

    def visit_key_value_pair(self, node):
        key, value = node.children
        return self.dispatch(key), self.dispatch(value)

    def visit_STRING(self, node):
        source = node.token.source  # type: str
        return source.strip('"')

    def visit_INTEGER(self, node):
        source = node.token.source  # type: str
        return int(source)

    def visit___0_true(self, node):
        return True

    def visit___1_false(self, node):
        return False

    def visit___2_null(self, node):
        return None

    def visit_FLOAT(self, node):
        source = node.token.source  # type: str
        return float(source)


def loads(s):
    ast = raw_loads(s)
    return Visitor().dispatch(ast)


def raw_loads(s):
    tree = parser(s)
    ast = to_ast.transform(tree)
    return ast
