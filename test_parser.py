import codecs
import glob
import os

import pytest

from purescript.parser import lexer, to_ast, module_parser, expression_parser, do_block_parser
from rpython.rlib.parsing.parsing import ParseError


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
ado_expression = """\
ado
    let
        x = l
    a <- x
in a
"""


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
    layout = [t.name for t in tokens if t.name in ["SEP", "INDENT", "DEDENT"]]
    assert layout == ["INDENT", "SEP", "DEDENT", "SEP"]
    do_block_parser.parse(tokens)


def test_parse_ado_block_expression():
    tokens = lexer.tokenize_with_name(
        "ado expression",
        ado_expression
    )
    expression_parser.parse(tokens)


def test_parse_do_expression():
    tokens = lexer.tokenize_with_name(
        "do expression",
        do_expression
    )
    expression_parser.parse(tokens)


def test_parse_if_then_else_expression():
    tokens = lexer.tokenize_with_name(
        "if_then_else",
        "if a then b else c"
    )
    expression_parser.parse(tokens)

files = [os.path.relpath(f) for glob_expression in [
    os.path.join(os.path.dirname(__file__), "test-data", "*.purs"),
    ] for f in glob.glob(glob_expression)]

assert files


@pytest.mark.parametrize("file_path", files)
def test_test_data(file_path):
    with open(file_path) as source_file:
        source = source_file.read()
    tokens = lexer.tokenize_with_name(file_path, source)
    try:
        module_parser.parse(tokens)
    except ParseError as e:
        message = e.nice_error_message(file_path, source, tokens)
        raise ValueError(message)
