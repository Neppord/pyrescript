import pytest

from purescript.lexer import human_name, level, layout_blocks
from purescript.parser import lexer
from rpython.rlib.parsing.lexer import Token, SourcePos

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
    assert [t.name for t in lexer.tokenize(text)] == ['STRING','SEP', 'EOF']


@pytest.mark.parametrize("text", [
    r'''"""\n"""''',
    r'''"""""""''',
])
def test_multiline_strings(text):
    assert [t.name for t in lexer.tokenize(text)] == ['MULTILINE_STRING','SEP',  'EOF']


@pytest.mark.parametrize(("text", "layout"), [
    (r'''''', ['SEP', 'EOF']),
    ('''\
a
    a
       a
    a
a''',
     [
         'LOWER', 'LOWER','LOWER','LOWER', 'SEP', 'LOWER','SEP',  'EOF'
     ]),
    ('''\
a
    a
       a
a''',
     [
         'LOWER', 'LOWER', 'LOWER', 'SEP', 'LOWER','SEP', 'EOF'
     ]),
])
def test_layout(text, layout):
    assert [t.name for t in lexer.tokenize(text)] == layout




def test_human_name():
    pos = SourcePos(0, 0, 0)
    assert human_name(Token("LINE_INDENT", "\n", pos)) == "LINE_INDENT"
    assert human_name(Token("__1_=", "\n", pos)) == "="


def test_level():
    pos = SourcePos(0, 0, 0)
    assert level(Token("LINE_INDENT", "\n", pos)) == 0
    assert level(Token("LINE_INDENT", "\n  ", pos)) == 2



def test_layout_blocks():
    pos = SourcePos(0, 0, 0)
    assert layout_blocks([Token("LINE_INDENT", "\n", pos)]) == [Token("SEP", "", pos)]
    assert layout_blocks([Token("LOWER", "a", pos)]) == [Token("LOWER", "a", pos)]


def test_layout_do_block():
    pos = SourcePos(0, 0, 0)
    tokens = layout_blocks([
        Token("do", "do", pos),
        Token("LINE_INDENT", "\n  ", pos), Token("LOWER", "a", pos),Token("LEFT_ARROW", "<-", pos),Token("LOWER", "a", pos),
        Token("LINE_INDENT", "\n  ", pos), Token("LOWER", "a", pos),
        Token("LINE_INDENT", "\n", pos),
    ])
    expect = [
        Token("do", "do", pos),
        Token("INDENT", "", pos), Token("LOWER", "a", pos),Token("LEFT_ARROW", "<-", pos),Token("LOWER", "a", pos), Token("SEP", "", pos),
        Token("LOWER", "a", pos), Token("SEP", "", pos),
        Token("DEDENT", "", pos), Token("SEP", "", pos),
    ]
    assert tokens == expect

def test_layout_do_block_same_level_with_where():
    pos = SourcePos(0, 0, 0)
    tokens = layout_blocks([
        Token("LINE_INDENT", "\n  ", pos), Token("do", "do", pos),
        Token("LINE_INDENT", "\n  ", pos), Token("LOWER", "a", pos),
        Token("LINE_INDENT", "\n  ", pos), Token("where", "where", pos),
        Token("LINE_INDENT", "\n  ", pos), Token("LOWER", "a", pos), Token("=", "=", pos), Token("INTEGER", "1", pos),
        Token("LINE_INDENT", "\n", pos),
    ])
    expect = [
        Token("do", "do", pos),
        Token("INDENT", "", pos), Token("LOWER", "a", pos), Token("SEP", "", pos),
        Token("DEDENT", "", pos), Token("SEP", "", pos),
        Token("where", "where", pos),
        Token("INDENT", "", pos), Token("LOWER", "a", pos), Token("=", "=", pos), Token("INTEGER", "1", pos), Token("SEP", "", pos),
        Token("DEDENT", "", pos), Token("SEP", "", pos),
    ]
    assert tokens == expect
