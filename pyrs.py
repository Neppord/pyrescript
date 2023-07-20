import sys
from purescript.parser import module_parser, lexer, compiled_module_parser, to_ast


def entry_point(argv):
    files_to_parse = argv[1:]
    for file_to_parse in files_to_parse:
        print "parsing file:", file_to_parse
        with open(file_to_parse) as f:
            source = f.read()
        tokens = lexer.tokenize_with_name(file_to_parse, source)
        tree = compiled_module_parser.parse(tokens)
        ast = to_ast.visit_module(tree)[0]
        print ast.children[0].token.source
    return 0


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    entry_point(sys.argv)
