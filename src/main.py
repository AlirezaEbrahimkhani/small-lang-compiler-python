import lexer

def main():
    
    # Read the current flow source code in input.lang and store it in variable
    content = ""
    with open("../tests/input.lang" , 'r') as file:
        content = file.read()
    
    #
    # Lexer
    #
        
    # Call the lexer class and initilize it with source code
    main_lexer = lexer.Lexer(content)
    main_lexer.lex()
     
main()