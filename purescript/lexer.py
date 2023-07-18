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


join_both_names = ["=", ","]
join_right_names = ["(", "[", "{"] + join_both_names
join_left_names = [")", "]", "}"] + join_both_names


def add_join_line(tokens):
    out = []
    for token in tokens:
        name = token.name.lstrip("_0123456789")
        if name in join_left_names:
            pos = token.source_pos
            out.append(Token("JLL", "", pos))
        out.append(token)
        if name in join_right_names:
            pos = token.source_pos
            offset = len(token.source)
            after_pos = SourcePos(
                pos.i + offset,
                pos.lineno,
                pos.columnno + offset,
            )
            out.append(Token("JLR", "", after_pos))
    return out


def join_lines(tokens):
    i = 0
    while i < len(tokens) - 1:
        t1 = tokens[i]
        t2 = tokens[i + 1]
        if t1.name == "JLR" and t2.name == "LINE_INDENT":
            del tokens[i + 1]
        elif t1.name == "LINE_INDENT" and t2.name == "JLL":
            del tokens[i]
            i = max(i - 1, 0)
        elif t1.name in ["JLL", "JLR"]:
            del tokens[i]
        else:
            i += 1
    return tokens


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

        tokens = add_join_line(result)
        tokens = join_lines(tokens)
        out = []
        current_level = 0
        stack = []
        for token in tokens:
            if token.name == "LINE_INDENT":
                source = token.source
                level = 0
                for char in source:
                    level += 1
                    if char == '\n':
                        level = 0
                if level > current_level:
                    token.name = "INDENT"
                    pos = token.source_pos
                    out.append(Token("SEP", '', pos))
                    out.append(token)
                    stack.append(current_level)
                    current_level = level
                elif level < current_level:
                    while level < current_level:
                        token.name = "DEDENT"
                        current_level = stack.pop()
                        pos = token.source_pos
                        out.append(Token("SEP", '', pos))
                        out.append(token)
                        out.append(Token("SEP", '', SourcePos(
                            pos.i + len(token.source),
                            pos.lineno + token.source.count("\n"),
                            current_level
                        )))
                else:
                    token.name = "SEP"
                    out.append(token)
            else:
                out.append(token)
        eof = out.pop()
        if out and out[-1].name != "SEP":
            out.append(Token("SEP", "", eof.source_pos))
        for _ in stack:
            out.append(Token("DEDENT", "", eof.source_pos))
            out.append(Token("SEP", "", eof.source_pos))
        out.append(eof)
        # remove empty lines
        i = 0
        while (i + 2) < len(out):
            t1 = out[i]
            t2 = out[i + 1]
            if t1.name == "DEDENT" and t2.name == "INDENT":
                t1.name = "SEP"
                t1.source += t2.source
                del out[i + 1]
                i -= 1
            elif t1.name == "SEP" and t2.name == "SEP":
                t1.source += t2.source
                del out[i + 1]
            else:
                i += 1

        return out
