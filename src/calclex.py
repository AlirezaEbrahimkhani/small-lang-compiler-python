import ply.lex as lex


class CalcLex(object):

    # List of token names. This is always required
    tokens = [
        'KEYWORD',
        'IDENTIFIER',
        'SPCIAL_CHARACTERS',
        'OPERATOR',
        'NUMBER',
        'STRING'
    ]

    # Regular expression rules for simple tokens
    t_KEYWORD = r"var|const|if|then|begin|end|integer|procedure|in|out|in out|print|read|for|to|do|return|call|not|and|or|else|string|bool"
    # t_IDENTIFIER = r'^[a-zA-Z_]+[a-zA-Z0-9_]*'
    t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_OPERATOR = r"(=)|(:=)|(<=)|(>=)|(>)|(<)|(<>)|(-)|(\+)|(/)|(\*)"
    t_SPCIAL_CHARACTERS = r"[$&,:;=?@#\|'<>.^*()%!]"
    t_STRING = r"\".*\"" ################################################################# yademon bashe nomre +

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'[.0-9]'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'
    t_ignore_COMMENT = r'\#.*'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # ----------------------------------------------------------------------
    # Ignored comments and blank lines  ################################################################# yademon bashe nomre +

    # comment (/* ... */)
    def t_COMMENT(self, t):
        r"""/\*(.|\n)*?\*/"""
        t.lexer.lineno += t.value.count('\n')

    # C++-style comment (//...)
    def t_CPPCOMMENT(self, t):
        r"""//.*\n"""
        t.lexer.lineno += 1

    def t_CPPCOMMENT2(self, t):
         r"""//.*"""
         t.lexer.lineno += 1


    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        value = ""
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break      # No more input
            value = value + str(tok)+"\n"
        return value