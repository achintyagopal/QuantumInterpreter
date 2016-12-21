import sys
from parser import Parser
from interpreter import Interpreter

def test():
    p = Parser(0)
    text = """
        int main(){
            int a;
            a = 3;
        }
        """

    p.parse_text(text)
    ast = p.get_ast()

    i = Interpreter(ast)
    i.interpret()


def run():
    if len(sys.argv) == 1:
        raise Exception("Missing input file")

    if len(sys.argv) > 2:
        raise Exception("Too many command line arguments")

    if len(sys.argv) == 2:
        data_file = sys.argv[1]

    test()
