import glob
import os

import pytest

from purescript.parser import lexer, module_parser, to_ast
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
    os.path.join(base, "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "Bootstrap.purs"),
    os.path.join(base, "css-frameworks", "v1.0.1", "src", "CSSFrameworks", "BoxIcons.purs"),
    os.path.join(base, "react-basic-dom", "v6.1.0", "src", "React", "Basic", "DOM", "Simplified", "Generated.purs"),
    os.path.join(base, "react-basic-dom", "v6.1.0", "src", "React", "Basic", "DOM", "Generated.purs"),
    os.path.join(base, "elmish-html", "v0.8.1", "src", "Elmish", "HTML", "Generated.purs"),
    os.path.join(base, "abc-parser", "v2.0.0", "test", "Midi.purs"),
    os.path.join(base, "abc-parser", "v2.0.0", "test", "KeySignature.purs"),
    os.path.join(base, "tecton", "v0.2.1", "src", "Tecton", "Internal.purs"),
    os.path.join(base, "jelly", "v0.10.0", "src", "Jelly", "Element.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Ai.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Bi.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Bs.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Cg.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Fa.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Gi.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Gr.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Hi.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Hi2.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Im.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Io.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Io5.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Md.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Ri.purs"),
    os.path.join(base, "react-icons", "v1.1.1", "src", "React", "Icons", "Tb.purs"),
    os.path.join(base, "unicode", "v6.0.0", "test", "Test", "Data", "CodePoint", "Unicode.purs"),
    os.path.join(base, "halogen-bootstrap5", "v2.2.0", "src", "Halogen", "Themes", "Bootstrap5.purs"),

}
dirname = os.path.dirname(__file__)
glob_expressions = [
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*.purs"),
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*", "*.purs"),
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*", "*", "*.purs"),
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*", "*", "*", "*.purs"),
        os.path.join(dirname, "e2e", "acme", ".spago", "*", "*", "*", "*", "*", "*", "*", "*.purs"),
    ]
parameters = []
for glob_expression in glob_expressions:
    for f in glob.glob(glob_expression):
        file_path_ = os.path.relpath(f)
        parameters.append(pytest.param(
            file_path_,
            marks=pytest.mark.skipif(file_path_ in slow, reason="slow test")
        ))

@pytest.mark.parametrize("file_path", parameters)
def test_e2e(file_path):
    with open(file_path) as source_file:
        source = source_file.read()
    tokens = lexer.tokenize_with_name(file_path, source)
    try:
        tree = module_parser.parse(tokens)
        # ast = to_ast.visit_module(tree)
    except ParseError as e:
        message = e.nice_error_message(file_path, source, tokens)
        raise ValueError(message)
