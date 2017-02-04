import os
import sys

from parser.parser import Parser
from interpreter.interpreter import Interpreter


def run():
    if len(sys.argv) == 1:
        raise Exception("Missing input file")

    if len(sys.argv) > 2:
        raise Exception("Too many command line arguments")

    if len(sys.argv) == 2:
        data_file = sys.argv[1]

    if not os.path.isfile(data_file):
        raise Exception(data_file + " does not exist")

    p = Parser()
    p.parse_file(data_file)
    ast = p.get_ast()

    i = Interpreter(ast)
    i.interpret()
