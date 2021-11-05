import os
import MainParser

# main method
def main():
    test_files = os.listdir("../tests")
    test_files.sort()
    output = open("./output.lang", "w")
    output2 = open("./output2.lang", "w")

    for file_name in test_files:
        with open("../tests/{}".format(file_name), 'r') as file:
            output.write("============================= {}".format(file_name) + " =============================\n")
            content = file.read()
            main_parser = MainParser.Parser()
            main_parser.buildLexer()
            result , pb = main_parser.build_parser(content)
            output.write(str(result)+"\n")
            output.write(str(main_parser.error_statement))
            output2.write("============================= {}".format(file_name) + " =============================\n")
            output2.write(pb+"\n")
    output.close()

main()
