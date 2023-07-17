from rpython.rlib.parsing.deterministic import LexerError
from rpython.rlib.parsing.lexer import Lexer, Token, SourcePos


class NiceLexerError(LexerError):
    def __init__(self, filename, input, state, source_pos):
        super(NiceLexerError, self).__init__(input, state, source_pos)
        self.filename = filename

    def __str__(self):
        return self.nice_error_message(filename=self.filename)


class IndentLexer(Lexer):
    def tokenize_with_name(self, name, text):
        try:
            return self.tokenize(text, True)
        except LexerError as e:
            raise NiceLexerError(name, e.input, e.state, e.source_pos)

    def tokenize(self, text, eof=False):
        tokens = super(IndentLexer, self).tokenize(text, True)
        out = []
        last_token = None
        current_level = 0
        stack = [current_level]
        for token in tokens:
            if token.name == "LINE_INDENT":
                level = len(token.source) - 1
                if level > current_level:
                    token.name = "INDENT"
                    out.append(token)
                    current_level = level
                    stack.append(current_level)
                elif level < current_level:
                    token.name = "DEDENT"
                    current_level = stack.pop()
                    out.append(Token("SEP",'',token.source_pos))
                    out.append(token)
                elif last_token and last_token.name == "SEP":
                    last_token.source += token.source
                    continue
                else:
                    token.name = "SEP"
                    out.append(token)
            else:
                out.append(token)
            last_token = token
        eof = out[-1]
        if out[-2].name != "SEP":
            out.insert(-1, Token("SEP", "", eof.source_pos))
        for level in stack[1:]:
            out.insert(-1, Token("DEDENT", "", eof.source_pos))
            out.insert(-1, Token("SEP", "", eof.source_pos))
        return out
