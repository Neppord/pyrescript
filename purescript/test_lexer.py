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


export_list = """\
module Main
  ( DBuffer
  , Offset

  , create
  )\
"""


def test_export_list():
    layout = [t.name for t in lexer.tokenize(export_list)]
    assert layout == [
        '__0_module',
        'PROPER_NAME',
        'INDENT',
        '__3_(',
        'PROPER_NAME',
        'SEP',
        '__5_,',
        'PROPER_NAME',
        'SEP',
        '__5_,',
        'LOWER',
        'SEP',
        '__4_)',
        'SEP',
        'DEDENT',
        'SEP',
        'EOF']


@pytest.mark.parametrize("text", [
    r'''"\""''',
    r'''"h"''',
    r'''"\n"''',
    r'''"""\n"""''',
])
def test_strings(text):
    assert [t.name for t in lexer.tokenize(text)] == ['STRING', 'SEP', 'EOF']
