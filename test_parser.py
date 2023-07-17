import os

from purescript.parser import lexer, to_ast, module_parser, expression_parser, do_block_parser
from rpython.rlib.parsing.lexer import SourcePos, Token


def test_loads_ebnf():
    assert True


def test_lex_simple_program():
    name = "Main.purs"
    with open(os.path.join("test-data", name)) as source_file:
        source = source_file.read()
    expected = [
        Token('__0_module', 'module', SourcePos(0, 0, 0)),
        Token('PROPER_NAME', 'Main', SourcePos(7, 0, 7)),
        Token('__1_where', 'where', SourcePos(12, 0, 12)),
        Token('SEP', '\n\n', SourcePos(17, 0, 17)),
        Token('__8_import', 'import', SourcePos(19, 2, 0)),
        Token('PROPER_NAME', 'Prelude', SourcePos(26, 2, 7)),
        Token('SEP', '\n\n', SourcePos(33, 2, 14)),
        Token('__8_import', 'import', SourcePos(35, 4, 0)),
        Token('PROPER_NAME', 'Effect', SourcePos(42, 4, 7)),
        Token('__3_(', '(', SourcePos(49, 4, 14)),
        Token('PROPER_NAME', 'Effect', SourcePos(50, 4, 15)),
        Token('__5_)', ')', SourcePos(56, 4, 21)),
        Token('SEP', '\n', SourcePos(57, 4, 22)),
        Token('__8_import', 'import', SourcePos(58, 5, 0)),
        Token('PROPER_NAME', 'Effect', SourcePos(65, 5, 7)),
        Token('__2_.', '.', SourcePos(71, 5, 13)),
        Token('PROPER_NAME', 'Console', SourcePos(72, 5, 14)),
        Token('__3_(', '(', SourcePos(80, 5, 22)),
        Token('LOWER', 'log', SourcePos(81, 5, 23)),
        Token('__5_)', ')', SourcePos(84, 5, 26)),
        Token('SEP', '\n\n', SourcePos(85, 5, 27)),
        Token('LOWER', 'main', SourcePos(87, 7, 0)),
        Token('__12_::', '::', SourcePos(92, 7, 5)),
        Token('__13_Effect Unit', 'Effect Unit', SourcePos(95, 7, 8)),
        Token('SEP', '\n', SourcePos(106, 7, 19)),
        Token('LOWER', 'main', SourcePos(107, 8, 0)),
        Token('__15_=', '=', SourcePos(112, 8, 5)),
        Token('LOWER', 'log', SourcePos(114, 8, 7)),
        Token('STRING', '"hello world!"', SourcePos(118, 8, 11)),
        Token('SEP', '\n', SourcePos(132, 8, 25)),
        Token('EOF', 'EOF', SourcePos(133, 9, 0))
    ]
    assert lexer.tokenize_with_name(name, source) == expected


def test_pars_simple():
    name = "Main.purs"
    with open(os.path.join("test-data", name)) as source_file:
        source = source_file.read()
    tokens = lexer.tokenize_with_name(name, source)
    tree = module_parser.parse(tokens)
    ast = to_ast.transform(tree)
    assert ast.symbol == "module"
    assert len([token for token in tokens if token.name == "SEP"]) == 6
    assert len(ast.children) == 6
    module_name, prelude, effect, effect_console, signature, main = ast.children
    assert module_name.symbol == "module_name"
    property_name, = module_name.children
    assert property_name.token.source == "Main"


call_expression = """\
log "hello world"
"""

call_declaration = """\
main = %s
""" % call_expression

do_expression = """\
do
    %s
""" % call_expression.strip()


def test_parse_call_expression():
    tokens = lexer.tokenize_with_name(
        "call_expression",
        call_expression
    )
    expression_parser.parse(tokens)


def test_parse_call_declaration():
    tokens = lexer.tokenize_with_name(
        "call_declaration",
        call_declaration
    )
    expression_parser.parse(tokens)


def test_parse_do_block():
    tokens = lexer.tokenize_with_name(
        "do expression",
        do_expression
    )
    layout = [t.name for t in tokens if t.name in ["SEP", "INDENT", "DEDENT"] ]
    assert layout == ["INDENT", "SEP", "DEDENT", "SEP"]
    do_block_parser.parse(tokens)

def test_parse_do_expression():
    tokens = lexer.tokenize_with_name(
        "do expression",
        do_expression
    )
    expression_parser.parse(tokens)


def test_parse_module_with_do():
    name = "MainWithDo.purs"
    with open(os.path.join("test-data", name)) as source_file:
        source = source_file.read()
    tokens = lexer.tokenize_with_name(name, source)
    tree = module_parser.parse(tokens)
    ast = to_ast.transform(tree)
    assert ast.symbol == "module"
    assert len(ast.children) == 6
    module_name, prelude, effect, effect_console, signature, main = ast.children
    assert module_name.symbol == "module_name"
    property_name, = module_name.children
    assert property_name.token.source == "Main"
