from types.inttype import IntType
from types.booltype import BoolType
from types.voidtype import VoidType
from types.arraytype import ArrayType

from nodes.arithmeticnode import ArithmeticNode
from nodes.assignnode import AssignNode
from nodes.boolnode import BoolNode
from nodes.callnode import CallNode
from nodes.compoundnode import CompoundNode
from nodes.conditionnode import ConditionNode
from nodes.functionnode import FunctionNode
from nodes.ifnode import IfNode
from nodes.indexnode import IndexNode
from nodes.intnode import IntNode
from nodes.logicnode import LogicNode
from nodes.newvariablenode import NewVariableNode
from nodes.notnode import NotNode
from nodes.paramsnode import ParamsNode
from nodes.returnnode import ReturnNode
from nodes.statementsnode import StatementsNode
from nodes.variablenode import VariableNode
from nodes.whilenode import WhileNode
from nodes.printnode import PrintNode


class AST:
    def __init__(self, debug_level = 0):
        self.debug = debug_level
        self.program = []

    def parse_word(self, text, loc, args):

        if self.debug > 0:
            print "Word:", args

        return [VariableNode(args[0])]

    def parse_int(self, text, loc, args):

        if self.debug > 0:
            print "Int:", args

        return [IntNode(args[0])]

    def parse_bool(self, text, loc, args):

        if self.debug > 0:
            print "Boolean:", args

        return [BoolNode(args[0])]

    def parse_type(self, text, loc, args):

        if self.debug > 0:
            print "Type:", args

        arg_type = str(args[0])
        if arg_type == "int":
            return [IntType()]
        elif arg_type == "bool":
            return [BoolType()]
        elif arg_type == "void":
            return [VoidType()]
        else:
            raise Exception("Type not handled")

    def parse_variable(self, text, loc, args):

        if self.debug > 0:
            print "Variable:", args

        if len(args) == 1:
            return args
        elif len(args) == 2:
            return [IndexNode(args[0], args[1])]
        else:
            raise Exception("Too many arguments")
            # return args

    def parse_variable_statement(self, text, loc, args):

        if self.debug > 0:
            print "Variable Statement:", args

        if len(args) == 2:
            if isinstance(args[1], IndexNode):
                array_size = args[1].get_index()
                variable_name = args[1].get_name()
                var_type = ArrayType(args[0], array_size)
            else:
                variable_name = args[1]
                var_type = args[0]
        else:
            raise Exception("Parse wrong")

        return [NewVariableNode(variable_name, var_type)]

    def parse_params(self, text, loc, args):

        if self.debug > 0:
            print "Params:", args

        return [ParamsNode(args)]

    def parse_statements(self, text, loc, args):

        if self.debug > 0:
            print "Statements:", args

        return [StatementsNode(args)]

    def parse_function(self, text, loc, args):

        if self.debug > 0:
            print "Function:", args

        if len(args) != 4:
            raise Exception("Incorrect function rule")

        return [FunctionNode(args[1], args[2], args[3], args[0])]

    def parse_program(self, text, loc, args):

        if self.debug > 0:
            print "Program:", args

        for arg in args:
            self.program.append(arg)

    def parse_return_statement(self, text, loc, args):

        if self.debug > 0:
            print "Return:", args

        if len(args) == 1:
            return [ReturnNode(None)]
        elif len(args) == 2:
            return [ReturnNode(args[1])]
        else:
            raise Exception("Return statement incorrect")

    def parse_if_statement(self, text, loc, args):

        if self.debug > 0:
            print "If:", args

        false_expr = None

        if len(args) == 3:
            condition = args[1]
            true_expr = args[2][0]
        elif len(args) == 5:
            condition = args[1]
            true_expr = args[2][0]
            false_expr = args[4][0]
        else:
            raise Exception("If statement rule incorrect")

        return [IfNode(condition, true_expr, false_expr)]

    def parse_while_statement(self, text, loc, args):

        if self.debug > 0:
            print "While:", args

        if len(args) == 3:
            condition = args[1]
            expression = args[2][0]
            return [WhileNode(condition, expression)]
        else:
            raise Exception("While statement rule incorrect")

    def parse_compound_statement(self, text, loc, args):

        if self.debug > 0:
            print "Compound:", args

        return [CompoundNode(args)]

    def parse_expression(self, text, loc, args):

        if self.debug > 0:
            print "Expression:", args

        if len(args) % 2 != 1:
            raise Exception("Expression incorrect")

        simple_expr = args[0]
        for i in range(1, len(args), 2):
            op = args[i]
            right = args[i + 1]

            if op in ("<", "<=", ">", ">=", "=="):
                simple_expr = ConditionNode(op, simple_expr, right)
            elif op == "=":
                simple_expr = AssignNode(simple_expr, right)
            else:
                raise Exception("Incorrect operand")

        return [simple_expr]

    def parse_call(self, text, loc, args):

        if self.debug > 0:
            print "Call:", args

        if len(args) == 1:
            return args

        if len(args) == 2:
            raise Exception("Call rule incorrect")

        if args[1] != "(":
            raise Exception("Call rule incorrect")

        if args[-1] != ")":
            raise Exception("Call rule incorrect")

        params = args[2:-1]
        return [CallNode(args[0], params)]

    def parse_not(self, text, loc, args):

        if self.debug > 0:
            print "Not:", args

        if len(args) != 1:
            raise Exception("Not rule incorrect")

        return [NotNode(args[0][0])]

    def parse_term(self, text, loc, args):

        if self.debug > 0:
            print "Term:", args

        if len(args) % 2 != 1:
            raise Exception("Term rule incorrect")

        term = args[0][0]
        for i in range(1, len(args), 2):
            op = args[i]
            right = args[i+1][0]

            if op in ("*", "/", "%"):
                term = ArithmeticNode(op, term, right)
            elif op == "&&":
                term = LogicNode(op, term, right)
            else:
                raise Exception("Incorrect operand")

        return [term]

    def parse_simple_expression(self, text, loc, args):

        if self.debug > 0:
            print "Simple Expression:", args

        start_index = 1
        if args[0] in ("+", "-"):
            if len(args) % 2 != 0:
                raise Exception("Term rule incorrect")
            expression = IntNode("0")
            expression = ArithmeticNode(args[0], expression, args[1])
            start_index = 2
        else:
            if len(args) % 2 != 1:
                raise Exception("Term rule incorrect")
            expression = args[0]

        for i in range(start_index, len(args), 2):
            op = args[i]
            right = args[i+1]

            if op in ("+", "-"):
                expression = ArithmeticNode(op, expression, right)
            elif op == "||":
                expression = LogicNode(op, expression, right)
            else:
                raise Exception("Incorrect operand")

        return [expression]

    def parse_print(self, text, loc, args):

        if self.debug > 0:
            print "Print:", args

        return [PrintNode(args)]
