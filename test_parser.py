import codecs
import glob
import os

import pytest

from purescript.parser import lexer, to_ast, module_parser, expression_parser, do_block_parser, type_parser
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
    expression_parser.parse(tokens)


do_expression = """\
do
    log "hello world"
""".strip()
ado_expression = """\
ado
    let
        x = l
    a <- x
in a
"""


@pytest.mark.parametrize("expression", [
    "if a then b else c",
    do_expression,
    ado_expression,
])
def test_parse_expression(expression):
    tokens = lexer.tokenize_with_name(
        "expression",
        expression
    )
    expression_parser.parse(tokens)


@pytest.mark.parametrize("file_path", [
    os.path.relpath(f)
    for f in glob.glob(os.path.join(os.path.dirname(__file__), "test-data", "*.purs"))
])
def test_test_data(file_path):
    with open(file_path) as source_file:
        source = source_file.read()
    tokens = lexer.tokenize_with_name(file_path, source)
    try:
        module_parser.parse(tokens)
    except ParseError as e:
        message = e.nice_error_message(file_path, source, tokens)
        raise ValueError(message)
