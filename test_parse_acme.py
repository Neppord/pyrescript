import glob
import os

import pytest

from purescript.parser import lexer, module_parser
from rpython.rlib.parsing.parsing import ParseError

files = {os.path.relpath(f) for glob_expression in [
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
] for f in glob.glob(glob_expression)}
skip = {
    os.path.join("e2e", "acme", ".spago", "unicode", "v6.0.0", "src", "Data", "CodePoint", "Unicode", "Internal.purs"),
    os.path.join("e2e", "acme", ".spago", "unicode", "v6.0.0", "src", "Data", "CodePoint", "Unicode", "Internal", "Casing.purs"),
    os.path.join("e2e", "acme", ".spago", "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "FontAwesome.purs"),
    os.path.join("e2e", "acme", ".spago", "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "TablerIcons.purs"),
    os.path.join("e2e", "acme", ".spago", "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "Primer.purs"),
    os.path.join("e2e", "acme", ".spago", "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "RemixIcon.purs"),
    os.path.join("e2e", "acme", ".spago", "react-basic-dom", "v6.1.0", "src", "React", "Basic", "DOM", "Simplified", "Generated.purs"),
    os.path.join("e2e", "acme", ".spago", "react-basic-dom", "v6.1.0", "src", "React", "Basic", "DOM", "Generated.purs"),
    os.path.join("e2e", "acme", ".spago", "elmish-html", "v0.8.1", "src", "Elmish", "HTML", "Generated.purs"),
}

assert files


@pytest.mark.parametrize("file_path", files - skip)
def test_e2e(file_path):
    with open(file_path) as source_file:
        source = source_file.read()
    tokens = lexer.tokenize_with_name(file_path, source)
    try:
        module_parser.parse(tokens)
    except ParseError as e:
        message = e.nice_error_message(file_path, source, tokens)
        raise ValueError(message)
