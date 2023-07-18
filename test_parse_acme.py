import glob
import os

import pytest

from purescript.parser import lexer, module_parser
from rpython.rlib.parsing.parsing import ParseError

files = [os.path.relpath(f) for glob_expression in [
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "src", "*.purs"),
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "src", "*", "*.purs"),
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "src", "*", "*", "*.purs"),
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "src", "*", "*", "*", "*.purs"),
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "src", "*", "*", "*", "*", "*.purs"),
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "test", "*.purs"),
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "test", "*", "*.purs"),
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "test", "*", "*", "*.purs"),
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "test", "*", "*", "*", "*.purs"),
    os.path.join(os.path.dirname(__file__), "e2e", "acme", ".spago", "*", "*", "test", "*", "*", "*", "*", "*.purs"),
] for f in glob.glob(glob_expression)]

assert files


@pytest.mark.parametrize("file_path", files)
def test_e2e(file_path):
    with open(file_path) as source_file:
        source = source_file.read()
    tokens = lexer.tokenize_with_name(file_path, source)
    try:
        module_parser.parse(tokens)
    except ParseError as e:
        message = e.nice_error_message(file_path, source, tokens)
        raise ValueError(message)
