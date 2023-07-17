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

        tokens = result
        out = []
        last_token = None
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
                    out.append(token)
                    stack.append(current_level)
                    current_level = level
                elif level < current_level:
                    token.name = "DEDENT"
                    current_level = stack.pop()
                    out.append(Token("SEP", '', token.source_pos))
                    out.append(token)
                elif last_token and last_token.name == "SEP":
                    last_token.source += source
                    continue
                else:
                    token.name = "SEP"
                    out.append(token)
            else:
                out.append(token)
            last_token = token
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
