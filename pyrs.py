import sys
from purescript.parser import module_parser, lexer


def entry_point(argv):
    files_to_parse, = argv[1:]
    for file_to_parse in files_to_parse:
        print "parsing file:", file_to_parse
        with open(file_to_parse) as f:
            source = f.read()
        tokens = lexer.tokenize_with_name(file_to_parse, source)
        module_parser.parse(tokens)
    return 0


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    entry_point(sys.argv)
