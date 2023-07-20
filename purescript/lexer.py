from rpython.rlib.parsing.deterministic import LexerError
from rpython.rlib.parsing.lexer import Lexer, Token, SourcePos


class NiceLexerError(Exception):
    def __init__(self, tokens, filename, input, state, source_pos):
        self.tokens = tokens
        self.filename = filename
        self.input = input
        self.state = state
        self.source_pos = source_pos

    def __str__(self):
        # + 1 is because source_pos is 0-based and humans 1-based
        columnno = self.source_pos.columnno
        lineno = self.source_pos.lineno
        i = self.source_pos.i
        lines = self.input.split("\n")
        result = ['"%s:%s:%s"' % (self.filename, lineno + 1, columnno + 1)]
        line = lines[lineno]
        result.append(repr(line))
        result.append(line)
        result.append(" " * columnno + "^")
        result.append("found %r" % (self.input[i],))
        result.append("context %r" % (self.input[max(0, i - 5):i + 3],))
        result.append("state: %r" % (self.state,))
        tokens = self.tokens
        if tokens and len(tokens) >= 3:
            result.append("last tokens: %r" % ([t.name for t in tokens[-3:]],))
        return "\n".join(result)



BLOCK_OWNERS = ["do", "ado", "let", "where", "of"]
def layout_blocks(tokens):
    blocks = []
    out = []
    indent = 0
    for index, token in enumerate(tokens):
        name = human_name(token)
        if name == "LINE_INDENT":
            if indent == level(token):
                if not out or out[-1].name not in ["SEP", "INDENT"]:
                    out.append(Token("SEP", "", token.source_pos))
            elif indent > level(token):
                while indent > level(token):
                    if not out or out[-1].name not in ["SEP", "INDENT"]:
                        out.append(Token("SEP", "", token.source_pos))
                    out.append(Token("DEDENT", "", token.source_pos))
                    out.append(Token("SEP", "", token.source_pos))
                    if blocks:
                        indent = blocks.pop()
                    else:
                        indent = 0
                        break
            else:
                pass
        elif name == "EOF":
            if indent == 0:
                if not out or out[-1].name not in ["SEP", "INDENT"]:
                    out.append(Token("SEP", "", token.source_pos))
            elif indent > 0:
                while indent > 0:
                    if not out or out[-1].name not in ["SEP", "INDENT"]:
                        out.append(Token("SEP", "", token.source_pos))
                    out.append(Token("DEDENT", "", token.source_pos))
                    out.append(Token("SEP", "", token.source_pos))
                    if blocks:
                        indent = blocks.pop()
                    else:
                        indent = 0
                        break
            else:
                pass
            out.append(token)
        elif name in BLOCK_OWNERS:
            next_token = tokens[index + 1]
            next_indent = level(next_token)
            if indent != 0 and next_indent == indent:
                # these blocks are siblings
                if not out or out[-1].name not in ["SEP", "INDENT"]:
                    out.append(Token("SEP", "", token.source_pos))
                out.append(Token("DEDENT", "", token.source_pos))
                out.append(Token("SEP", "", token.source_pos))
            out.append(token)
            if human_name(next_token) == "LINE_INDENT" and next_indent >= indent:
                if next_indent != indent or indent == 0:
                    blocks.append(indent)
                indent = next_indent
                out.append(Token("INDENT", "", next_token.source_pos))
        else:
            out.append(token)
    return out


def human_name(token):
    if token.name.startswith("__"):
        # the internal names looks like so __\d+_name
        without_prefix = token.name[2:]
        number_, _, name = without_prefix.partition("_")
        return name
    return token.name


def level(line_indent):
    ret = 0
    for c in line_indent.source:
        if c == "\n":
            ret = 0
        else:
            ret += 1
    return ret

class IndentLexer(Lexer):
    def tokenize_with_name(self, name, text):
        try:
            return self.tokenize(text, True)
        except NiceLexerError as e:
            raise NiceLexerError(e.tokens, name, e.input, e.state, e.source_pos)

    def tokenize(self, text, eof=False):
        # tokens = super(IndentLexer, self).tokenize(text, True)
        r = self.get_runner(text, True)
        result = []
        while 1:
            try:
                tok = r.find_next_token()
                result.append(tok)
            except StopIteration:
                break
            except LexerError as e:
                raise NiceLexerError(result, "<None>", text, e.state, e.source_pos)
        return layout_blocks(result)
