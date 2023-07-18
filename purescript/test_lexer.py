import pytest

from purescript.parser import lexer

almost_empty = """\

"""


def test_almost_empty():
    layout = [t.name for t in lexer.tokenize(almost_empty)]
    assert layout == ["SEP", "EOF"]


empty_line = """\
  

  

"""


def test_empty_line():
    layout = [t.name for t in lexer.tokenize(empty_line)]
    assert layout == ['SEP', 'EOF']


@pytest.mark.parametrize("text", [
    r'''"\""''',
    r'''"h"''',
    r'''"\n"''',
])
def test_strings(text):
    assert [t.name for t in lexer.tokenize(text)] == ['STRING', 'SEP', 'EOF']


@pytest.mark.parametrize("text", [
    r'''"""\n"""''',
    r'''"""""""''',
])
def test_multiline_strings(text):
    assert [t.name for t in lexer.tokenize(text)] == ['MULTILINE_STRING', 'SEP', 'EOF']


@pytest.mark.parametrize(("text", "layout"), [
    (r'''''', ['EOF']),
    ('''\
a
    a
       a
    a
a''',
     [
         'LOWER', 'SEP',
         'INDENT', 'LOWER', 'SEP',
         'INDENT', 'LOWER', 'SEP',
         'DEDENT', 'SEP', 'LOWER', 'SEP',
         'DEDENT', 'SEP', 'LOWER', 'SEP',
         'EOF'
     ]),
    ('''\
a
    a
       a
a''',
     [
         'LOWER', 'SEP',
         'INDENT', 'LOWER', 'SEP',
            'INDENT', 'LOWER', 'SEP', 'DEDENT', 'SEP',
         'DEDENT', 'SEP', 'LOWER', 'SEP',
         'EOF'
     ]),
])
def test_layout(text, layout):
    assert [t.name for t in lexer.tokenize(text)] == layout
