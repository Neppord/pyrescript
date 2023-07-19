import glob
import os

import pytest

from purescript.parser import lexer, module_parser
from rpython.rlib.parsing.parsing import ParseError

base = os.path.join("e2e", "acme", ".spago")
slow = {
    os.path.join(base, "unicode", "v6.0.0", "src", "Data", "CodePoint", "Unicode", "Internal.purs"),
    os.path.join(base, "unicode", "v6.0.0", "src", "Data", "CodePoint", "Unicode", "Internal", "Casing.purs"),
    os.path.join(base, "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "FontAwesome.purs"),
    os.path.join(base, "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "TablerIcons.purs"),
    os.path.join(base, "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "Primer.purs"),
    os.path.join(base, "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "RemixIcon.purs"),
    os.path.join(base, "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "BootstrapIcons.purs"),
    os.path.join(base, "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "BoxIcons.purs"),
    os.path.join(base, "react-basic-dom", "v6.1.0", "src", "React", "Basic", "DOM", "Simplified", "Generated.purs"),
    os.path.join(base, "react-basic-dom", "v6.1.0", "src", "React", "Basic", "DOM", "Generated.purs"),
    os.path.join(base, "elmish-html", "v0.8.1", "src", "Elmish", "HTML", "Generated.purs"),
}
dirname = os.path.dirname(__file__)


@pytest.mark.parametrize("file_path", {
    pytest.param(os.path.relpath(f), mark=pytest.mark.skipif(os.path.relpath(f) in slow, "slow test"))
    for glob_expression in [
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*.purs"),
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*", "*.purs"),
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*", "*", "*.purs"),
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*", "*", "*", "*.purs"),
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*", "*", "*", "*", "*.purs"),
    ] for f in glob.glob(glob_expression)
})
def test_e2e(file_path):
    with open(file_path) as source_file:
        source = source_file.read()
    tokens = lexer.tokenize_with_name(file_path, source)
    try:
        module_parser.parse(tokens)
    except ParseError as e:
        message = e.nice_error_message(file_path, source, tokens)
        raise ValueError(message)
