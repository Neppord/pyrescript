import glob
import os

import pytest

from purescript.parser import lexer, to_ast, module_parser, expression_parser, type_parser, \
    binder_parser, declaration_parser
from rpython.rlib.parsing.parsing import ParseError


@pytest.mark.parametrize("type_", [
    """forall a. a -> a""",
])
def test_parse_type(type_):
    tokens = lexer.tokenize_with_name("type", type_)
    assert type_parser.parse(tokens).symbol == "type"


@pytest.mark.parametrize("declaration", [
    '''main = log "hello world"'''
])
def test_parse_declaration(declaration):
    tokens = lexer.tokenize_with_name("declaration", declaration)
    declaration_parser.parse(tokens)


do_expression = """\
do
    log "hello world"
""".strip()
@pytest.mark.parametrize("expression", [
    "if a then b else c",
    "(1)",
    """f\n  1""",
    """let x = 1 in x""",
    do_expression,
    """ado a <- x in a""",
    """\
ado 
    let
        x = 1
in a\
""",
    """\
ado
    a <- x
    b <- y
in a\
    """,
])
def test_parse_expression(expression):
    file_path = "expression"
    tokens = lexer.tokenize_with_name(file_path, expression)
    try:
        expression_parser.parse(tokens)
    except ParseError as e:
        message = e.nice_error_message(file_path, expression, tokens)
        raise ValueError(message)

@pytest.mark.parametrize("binder", [
    "a",
    "{a}",
    "{a:b}",
    "{a, b}",
])
def test_parse_binder(binder):
    tokens = lexer.tokenize_with_name("binder", binder)
    binder_parser.parse(tokens)


@pytest.mark.parametrize("file_path", [
    os.path.relpath(f)
    for f in glob.glob(os.path.join(os.path.dirname(__file__), "test-data", "*.purs"))
])
def test_test_data(file_path):
    with open(file_path) as source_file:
        source = source_file.read()
    tokens = lexer.tokenize_with_name(file_path, source)
    try:
        tree = module_parser.parse(tokens)
        ast = to_ast.visit_module(tree)[0]
    except ParseError as e:
        message = e.nice_error_message(file_path, source, tokens)
        raise ValueError(message)
