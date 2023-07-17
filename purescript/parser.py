# coding=utf-8
import os

from purescript.lexer import IndentLexer
from rpython.rlib.parsing.ebnfparse import parse_ebnf, check_for_missing_names
from rpython.rlib.parsing.parsing import PackratParser

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


def parse_module(name, s):
    tokens = lexer.tokenize_with_name(name, s)
    return module_parser.parse(tokens)


regexes, rules, _to_ast = parse_ebnf(EBNF)
names, regexs = zip(*regexes)
to_ast = _to_ast()
all_names = list(names) + ["EOF", "SEP", "INDENT", "DEDENT"]
check_for_missing_names(all_names, regexs, rules)
lexer = IndentLexer(list(regexs), all_names, ignore=["IGNORE", "LINE_COMMENT", "MULTILINE_COMMENT"])
module_parser = PackratParser(rules, "module")
declaration_parser = PackratParser(rules, "declaration")
expression_parser = PackratParser(rules, "expression")
do_block_parser = PackratParser(rules, "do_block")



