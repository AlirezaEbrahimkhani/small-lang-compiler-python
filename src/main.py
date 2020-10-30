import lexer

def main():
    
    content = ""
    with open("../tests/input.lang" , 'r') as file:
        content = file.read()
    
    main_lexer = lexer.Lexer(content)
    main_lexer.lex()
     
main()