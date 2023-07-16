from purescript.parser import parse, lexer
from rpython.rlib.parsing.lexer import SourcePos, Token


def test_loads_ebnf():
    assert True


def test_lex_simple_program():
    assert lexer.tokenize_with_name(
"Main.purs",
"""module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)

main :: Effect Unit
main = log "hello world!"
"""
    ) == [Token('__0_module', 'module', SourcePos(0, 0, 0)),
 Token('PROPER_NAME', 'Main', SourcePos(7, 0, 7)),
 Token('__1_where', 'where', SourcePos(12, 0, 12)),
 Token('INDENT', '\n', SourcePos(17, 0, 17)),
 Token('INDENT', '\nimport', SourcePos(18, 1, 0)),
 Token('PROPER_NAME', 'Prelude', SourcePos(26, 2, 1)),
 Token('DEDENT', '\n', SourcePos(33, 2, 8)),
 Token('INDENT', '\nimport', SourcePos(34, 3, 0)),
 Token('PROPER_NAME', 'Effect', SourcePos(42, 4, 1)),
 Token('__3_(', '(', SourcePos(49, 4, 8)),
 Token('PROPER_NAME', 'Effect', SourcePos(50, 4, 9)),
 Token('__5_)', ')', SourcePos(56, 4, 15)),
 Token('SEP', '\nimport', SourcePos(57, 4, 16)),
 Token('PROPER_NAME', 'Effect', SourcePos(65, 5, 1)),
 Token('__2_.', '.', SourcePos(71, 5, 7)),
 Token('PROPER_NAME', 'Console', SourcePos(72, 5, 8)),
 Token('__3_(', '(', SourcePos(80, 5, 16)),
 Token('LOWER', 'log', SourcePos(81, 5, 17)),
 Token('__5_)', ')', SourcePos(84, 5, 20)),
 Token('DEDENT', '\n', SourcePos(85, 5, 21)),
 Token('INDENT', '\nmain', SourcePos(86, 6, 0)),
 Token('__12_::', '::', SourcePos(92, 7, 1)),
 Token('__13_Effect Unit', 'Effect Unit', SourcePos(95, 7, 4)),
 Token('SEP', '\nmain', SourcePos(106, 7, 15)),
 Token('__15_=', '=', SourcePos(112, 8, 1)),
 Token('LOWER', 'log', SourcePos(114, 8, 3)),
 Token('STRING', '"hello world!"', SourcePos(118, 8, 7)),
 Token('DEDENT', '\n', SourcePos(132, 8, 21))]



def test_lex_simple_program():
    assert lexer.tokenize_with_name(
"Main.purs",
"""module Main where

import Prelude

import Effect (Effect)
import Effect.Console (log)

main :: Effect Unit
main = do
  log "hello world!"
  log "hello again world!"
"""
    ) == [Token('__0_module', 'module', SourcePos(0, 0, 0)),
 Token('PROPER_NAME', 'Main', SourcePos(7, 0, 7)),
 Token('__1_where', 'where', SourcePos(12, 0, 12)),
 Token('INDENT', '\n', SourcePos(17, 0, 17)),
 Token('INDENT', '\nimport', SourcePos(18, 1, 0)),
 Token('PROPER_NAME', 'Prelude', SourcePos(26, 2, 1)),
 Token('DEDENT', '\n', SourcePos(33, 2, 8)),
 Token('INDENT', '\nimport', SourcePos(34, 3, 0)),
 Token('PROPER_NAME', 'Effect', SourcePos(42, 4, 1)),
 Token('__3_(', '(', SourcePos(49, 4, 8)),
 Token('PROPER_NAME', 'Effect', SourcePos(50, 4, 9)),
 Token('__5_)', ')', SourcePos(56, 4, 15)),
 Token('SEP', '\nimport', SourcePos(57, 4, 16)),
 Token('PROPER_NAME', 'Effect', SourcePos(65, 5, 1)),
 Token('__2_.', '.', SourcePos(71, 5, 7)),
 Token('PROPER_NAME', 'Console', SourcePos(72, 5, 8)),
 Token('__3_(', '(', SourcePos(80, 5, 16)),
 Token('LOWER', 'log', SourcePos(81, 5, 17)),
 Token('__5_)', ')', SourcePos(84, 5, 20)),
 Token('DEDENT', '\n', SourcePos(85, 5, 21)),
 Token('INDENT', '\nmain', SourcePos(86, 6, 0)),
 Token('__12_::', '::', SourcePos(92, 7, 1)),
 Token('__13_Effect Unit', 'Effect Unit', SourcePos(95, 7, 4)),
 Token('SEP', '\nmain', SourcePos(106, 7, 15)),
 Token('__15_=', '=', SourcePos(112, 8, 1)),
 Token('__17_do', 'do', SourcePos(114, 8, 3)),
 Token('DEDENT', '\n', SourcePos(116, 8, 5)),
 Token('LOWER', 'log', SourcePos(119, 9, 2)),
 Token('STRING', '"hello world!"', SourcePos(123, 9, 6)),
 Token('SEP', '\n', SourcePos(137, 9, 20)),
 Token('LOWER', 'log', SourcePos(140, 10, 2)),
 Token('STRING', '"hello again world!"', SourcePos(144, 10, 6)),
 Token('SEP', '\n', SourcePos(164, 10, 26))]
