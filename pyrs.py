import sys
from parser import ParserError

from purescript.lexer import NiceLexerError
from purescript.parser import module_parser, lexer, compiled_module_parser, to_ast


def entry_point(argv):
    files_to_parse = argv[1:]
    for file_to_parse in files_to_parse:
        print "parsing file:", file_to_parse
        with open(file_to_parse) as f:
            source = f.read()
        try:
            tokens = lexer.tokenize_with_name(file_to_parse, source)
        except NiceLexerError as e:
            print e
            return 1
        try:
            tree = compiled_module_parser.parse(tokens)
        except ParserError as e:
            print e
            return 1
        ast = to_ast.visit_module(tree)[0]
        module_name = ast.children[0]
        parts = []
        for child in module_name.children:
            parts.append(child.token.source)
        print ".".join(parts)
    return 0


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    entry_point(sys.argv)
