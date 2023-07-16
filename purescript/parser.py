# coding=utf-8
import os

from rpython.rlib.objectmodel import we_are_translated
from rpython.rlib.parsing.deterministic import LexerError
from rpython.rlib.parsing.ebnfparse import parse_ebnf, check_for_missing_names
from rpython.rlib.parsing.parsing import PackratParser
from rpython.rlib.parsing.lexer import Lexer

EBNF = "\n"
with open(os.path.join(os.path.dirname(__file__), "ebnf.md")) as ebnf_file:
    reading = False
    for line in ebnf_file:
        if line.startswith("```ebnf") and not reading:
            reading = True
            EBNF += "\n"
        elif line.startswith("```") and reading:
            reading = False
            EBNF += "\n"
        elif line.startswith("#") or not reading:
            EBNF += "\n"
        else:
            EBNF += line


def parse(s):
    tokens = lexer.tokenize(s, True)
    s = parser.parse(tokens)
    if not we_are_translated():
        try:
            if py.test.config.option.view:
                s.view()
        except AttributeError:
            pass
    return s

class NiceLexerError(LexerError):
    def __init__(self, filename, input, state, source_pos):
        super(NiceLexerError, self).__init__(input, state, source_pos)
        self.filename = filename

    def __str__(self):
        return self.nice_error_message(filename=self.filename)

class IndentLexer(Lexer):
    def tokenize_with_name(self, name, text, eof=False):
        try:
            return self.tokenize(text, eof=eof)
        except LexerError as e:
            raise NiceLexerError(name, e.input, e.state, e.source_pos)

    def tokenize(self, text, eof=False):
        tokens = super(IndentLexer, self).tokenize(text, eof)
        stack = [0]
        out = []
        for token in tokens:
            if token.name == "LINE_INDENT":
                level = len(token.source)
                current = stack[-1]
                if level > current:
                    token.name = "INDENT"
                    out.append(token)
                    stack.append(level)
                elif level < current:
                    token.name = "DEDENT"
                    stack.pop()
                    out.append(token)
                else:
                    token.name = "SEP"
                    out.append(token)
            else:
                out.append(token)
        return out



regexes, rules, _to_ast = parse_ebnf(EBNF)
names, regexs = zip(*regexes)
to_ast = _to_ast()

check_for_missing_names(list(names) + ["SEP", "INDENT", "DEDENT"], regexs, rules)
lexer = IndentLexer(list(regexs), list(names), ignore=["IGNORE"])
parser = PackratParser(rules, rules[0].nonterminal)



