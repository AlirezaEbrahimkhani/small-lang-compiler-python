class Lexer:
    
     # Define all regex
    RE_KEYWORD = "var|const|if|then|begin|end|integer|procedure|in|out|in out|print|read|for|to|do|return|call|not|and|or|else|string|bool"
    RE_IDENTIFIER = "^[a-zA-Z_]+[a-zA-Z0-9_]*"
    RE_NUMERAL = "[.0-9]"
    RE_OPERATOR = "(=)|(:=)|(<=)|(>=)|(>)|(<)|(<>)|(-)|(\+)|(/)|(\*)"
    RE_SPCIAL_CHARACTERS = "[$&+,:;=?@#|'<>.^*()%!-]"
    
    def __init__(self , source_code):
        self.source_code = source_code
    
    def lex(self):
        