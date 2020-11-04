import lexer
import os

# main method
def main():
    
    # Read the current flow source code in input.lang and store it in variable
    content = ""
    test_files = os.listdir("../tests/")
    test_files.sort()
    for file_name in test_files:
        with open("../tests/{}".format(file_name) , 'r') as file:
            content = file.read()
        #
        # Lexer
        #
            print("============================= {}".format(file_name)," =============================\n")
        # Call the lexer class and initilize it with source code
            main_lexer = lexer.Lexer(content)
            lexer_result = list(main_lexer.lex())
            
            for result in lexer_result:
                print(result , "\n")
        
main()