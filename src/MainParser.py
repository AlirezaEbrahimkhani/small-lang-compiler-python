from ply import lex
import ply.yacc as yacc
import re

symbols = {}

class Parser():

    pb = ""

    tokens = (
        'IDENTIFIER',
        'EQUALS',
        'OPERATOR',
        'NUMBER',
        'STRING',
        'PLUS',
        'MINUS',
        'DIV',
        'TIMES',
        'LPAREN',
        'RPAREN',
        'SEMI',
        'LBRAKET',
        'RBRAKET',
        'COMMA',
        'COLON'
    )

    reserved = {
        'print': 'PRINT',
        'read': 'READ',
        'return': 'RETURN',
        'call': 'CALL',
        'not': 'NOT',
        'and': 'AND',
        'or': 'OR',
        'if': 'IF',
        'else': 'ELSE',
        'then': 'THEN',
        'for': 'FOR',
        'to': 'TO',
        'do': 'DO',
        'in': 'IN',
        'out': 'OUT',
        'integer': 'INTEGER',
        'char': 'CHAR',
        'float': 'FLOAT',
        'double': 'DOUBLE',
        'boolean': 'BOOLEAN',
        'string': 'STRINGTYPE',
        'procedure': 'PROCEDURE',
        'begin': 'BEGIN',
        'const': 'CONST',
        'var': 'VAR',
        'end': 'END'
    }

    t_COMMA = r","
    t_OPERATOR = r"(=)|(<=)|(>=)|(>)|(<>)|(<)"
    t_EQUALS = r':='
    t_SEMI = r';'
    #   t_SPCIAL_CHARACTERS = r"[$&?@#\|'.^%!]"
    t_STRING = r"\".*\""
    t_ignore = ' \t'
    t_ignore_COMMENT = r'\#.*'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRAKET = r'\['
    t_RBRAKET = r'\]'
    t_MINUS = r'-'
    t_PLUS = r'\+'
    t_TIMES = r'\*'
    t_DIV = r'/'
    t_COLON = r':'

    tokens = list(tokens) + list(reserved.values())

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # Check for reserved words
        t.type = self.reserved.get(t.value.lower(), 'IDENTIFIER')
        return t

    def t_NUMBER(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

    def t_CPPCOMMENT(self, t):
        r'//.*\n'
        t.lexer.lineno += 1

    def buildLexer(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    error_statement = ""

    precedence = (
        ('left', 'STATELIST'),
        ('left', 'DECLLIST'),
        ('left', 'CONDLIST'),
        ('left', 'IF'),
        ('left', 'ELSE'),
        ('left', 'OPERATOR'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIV'),
        ('nonassoc', 'UMINUS')
    )

    def p_program(self, p):
        '''program : const_repeat var_repeat ex_procedure BEGIN circular_statement END SEMI'''

    def p_ex_procedure(self, p):
        '''ex_procedure : circular_procedure
                            | '''

    def p_circular_procedure(self, p):
        '''circular_procedure : procedure %prec DECLLIST
                          | circular_procedure procedure'''

    def p_circular_statement(self, p):
        '''circular_statement : statement %prec STATELIST
                          | circular_statement statement'''

    def p_procedure(self, p):
        '''procedure : PROCEDURE IDENTIFIER LPAREN circular_format RPAREN COLON block'''

    def p_block(self, p):
        '''block : BEGIN const_repeat var_repeat optional_statement END SEMI'''

    def p_optional_statement(self, p):
        '''optional_statement : statement
                          |  '''

    def p_const_repeat(self, p):
        '''const_repeat : circular_const %prec DECLLIST
                    |
        circular_const : CONST const_decl
                    | circular_const CONST const_decl'''

    def p_var_repeat(self, p):
        '''var_repeat : circular_var %prec DECLLIST
                  |
        circular_var : VAR var_decl
                  | circular_var VAR var_decl'''

    def p_var_decl(self, p):
        '''var_decl : circular_id COLON type SEMI'''
        for x in list(p[1]):
            if x in symbols.keys():
                self.p_error("!!Error!! : {}:{}".format(self.lexer.lineno - 1,"Duplicate Identifier Definition ...!"))

            else:
                symbols[x] = p[3]

    def p_const_decl(self, p):
        '''const_decl : circular_id EQUALS NUMBER SEMI'''
        for x in list(p[1]):
            if x in symbols.keys():
                self.p_error("!!Error!! : {}:{}".format(self.lexer.lineno - 1,"Duplicate Identifier Definition ...!"))


            else:
                symbols[x] = 'integer'

    def p_circular_format(self, p):
        '''circular_format : format
                       | circular_format COLON format
                       |  '''

    def p_format(self, p):
        '''format : circular_id COLON mode type'''

    def p_circular_id(self, p):
        '''circular_id : IDENTIFIER
                   | circular_id COMMA IDENTIFIER'''
        if len(p) <= 3:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[3]
        # if str(p[1]) != 'None':
        #     p[0] = p[1]
        #     print(p[1])
        # else:
        #     p[0] = p[3]
        #     print(p[3])

    def p_type(self, p):
        '''type : INTEGER
            | STRINGTYPE
            | CHAR
            | FLOAT
            | DOUBLE
            | BOOLEAN'''
        p[0] = p[1]

    def p_mode(self, p):
        '''mode : IN
            | OUT
            | IN OUT
            |  '''

    def p_statement(self, p):
        '''statement : print
                 | asgn
                 | read
                 | return
                 | call
                 | cond
                 | for'''
        p[0] = p[1]

    def p_cond(self, p):
        '''cond : IF bool THEN statement %prec IF
            | IF bool THEN statement ELSE statement'''
            
        self.pb = self.pb + "\n" + \
                  "({} , {} , {} , )".format(
                      list(p[4])[1] + str((list(p[4])[2])), str(id(list(p[4])[0])), id(list(p[4])[3]))

        self.pb = self.pb + "\n" + \
                  "(JP , {} , , )".format(self.lexer.lineno)
        
        self.pb = self.pb + "\n" + \
                  "({} , {} , {} , )".format(
                      list(p[6])[1] + list(p[6])[2], id(list(p[6])[0]), id(list(p[6])[3]))
            

    def p_bool(self, p):
        '''bool : NOT bool %prec CONDLIST
            | bool AND bool %prec CONDLIST
            | bool OR bool %prec CONDLIST
            | LPAREN bool RPAREN
            | expr OPERATOR expr'''  # CONDLIST dare mige age 2 ta bool kenar ham dashte bashim mes adam bahashon raftar kon va hich taghadomi nadashte bash
        p[0] = p[1] + p[2] + p[3]
        self.pb = self.pb + "\n" + "({} , {} , {} , {})".format(p[2], id(p[1]), id(p[3]), id(p[0]))
        self.pb = self.pb + "\n" + "(JPF , {} , {} , )".format(id(p[0]), self.lexer.lineno + 3)

    def p_for(self, p):
        '''for : FOR IDENTIFIER EQUALS expr TO expr DO statement'''

    def p_call(self, p):
        '''call : CALL IDENTIFIER LPAREN args RPAREN SEMI'''

    def p_args(self, p):
        '''args : expr
            | args COMMA expr
            |  '''

    def p_return(self, p):
        'return : RETURN SEMI'

    def p_read(self, p):
        '''read : READ LPAREN var_value RPAREN SEMI'''

    def p_var_value(self, p):
        '''var_value : var
                 | STRING
                 | var_value COMMA var'''

    def p_value(self, p):
        '''value : expr
             | STRING
             | value COMMA expr'''
        # if len(self,p) <= 3:
        #     p[0] = [p[1]]
        # else:
        #     p[0] = p[1] + [p[3]]

    def p_print(self, p):
        '''print : PRINT LPAREN value RPAREN SEMI'''
        # p[0] = p[3]

    def p_asgn(self, p):
        'asgn : var EQUALS expr SEMI'
        p[0] = str(p[1]) + str(p[2]) + str(p[3])
        if p[1] not in symbols.keys():
            self.p_error("!!Error!! : {}:{}".format(self.lexer.lineno - 1,"You should Define your variable ...!"))
        else:
            var_type = symbols.get(p[1]);
            if re.match(r'[0-9]+' ,str(p[3])):
                if var_type != 'integer':
                    self.p_error("!!Error!! : {}:{}".format(self.lexer.lineno - 1,"Invalid variable assignment ...!"))
            elif re.match(r'[a-zA-Z_][a-zA-Z_0-9]*' , p[3]):
                if p[3] in symbols.keys():
                    id_type = symbols.get(p[3])
                    if id_type != var_type:
                       self.p_error("!!Error!! : {}:{}".format(self.lexer.lineno - 1,"Invalid variable assignment ...!"))
                else:
                    self.p_error("!!Error!! : {}:{}".format(self.lexer.lineno - 1,"You should Define your variable ...!"))

    def p_expr(self, p):
        '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
          | expr DIV expr'''

        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        else:
            p[0] = p[1] / p[3]
            
        self.pb = self.pb + "\n" + str("({} , {} , {} , {})".format(p[2], id(p[1]), id(p[3]), id(p[0])))
    
    def p_expr2uminus(self, p):
        'expr : MINUS expr %prec UMINUS'
        p[0] = - p[2]

    def p_integer_constant(self, p):
        '''expr : NUMBER
            | var'''
        p[0] = p[1]

    def p_parens(self, p):
        'expr : LPAREN expr RPAREN'
        p[0] = p[2]

    def p_var(self, p):
        'var : IDENTIFIER braket'
        p[0] = p[1]

    def p_braket(self, p):
        '''braket : braket LBRAKET expr RBRAKET
              |  '''

    def p_error(self, p):
        if str(p).split(':')[0] == "!!Error!! ":
            data = str(p).split(':');
            self.error_statement += "!! Error !! : Line({}) => {}".format(
                data[1][1:], data[2]) + "\n"
        elif str(p) != 'None':
            line = str(p).split(',')[2]
            token = str(p).split(',')[0].split('(')[1]
            self.error_statement += "!! Error !! : Line({}) => Error near {}".format(
                line, token) + "\n"
        else:
            self.error_statement += "Syntax Error in input" + "\n"

    def build_parser(self, code):
        self.parser = yacc.yacc(module=self)
        res = self.parser.parse(code)
        symbols.clear();
        yield res
        yield self.pb