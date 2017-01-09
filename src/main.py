import sys
from parser import Parser
from interpreter import Interpreter


def test():
    p = Parser(0)
    text = """
        int main(){
            int a;
            a = 3 + 3;
            /* a(3);*/
            read(a);

            print(a);
            return 0;
        }
        """

    p.parse_text(text)
    ast = p.get_ast()

    i = Interpreter(ast, 0)
    i.interpret()


def run():
    if len(sys.argv) == 1:
        raise Exception("Missing input file")

    if len(sys.argv) > 2:
        raise Exception("Too many command line arguments")

    if len(sys.argv) == 2:
        data_file = sys.argv[1]

    test()
