import sys

from box.box import Box
from box.intbox import IntBox
from box.boolbox import BoolBox
from box.arraybox import ArrayBox

from environment import Environment
from scope import Scope
from returnstatement import ReturnStatement

from ..parser.types.voidtype import VoidType
from ..parser.types.inttype import IntType
from ..parser.types.booltype import BoolType
from ..parser.types.arraytype import ArrayType


class Interpreter():
    def __init__(self, ast, debug=0):
        self.ast = ast
        self.functions = {}
        self.stack = []
        self.env = Environment()
        self.environments = [self.env]
        self.function_locs = []
        self.debug = debug
        self.built_in_functions = ("print", "read")
        self.built_in_functions_map = {
            "print": self.__print,
            "read": self.__read
        }

    def interpret(self):

        for function in self.ast.program:
            fun_name = function.get_function_name()
            if fun_name in self.built_in_functions:
                raise Exception("Cannot overwrite a built-in function: " + str(self.built_in_functions))

            function_name = function.get_function_name_with_params()

            if self.functions.get(function_name) is not None:
                raise Exception(function_name + " already exists")

            self.functions[function_name] = function

        if self.functions.get("main_void") is None:
            return

        self.__interpret(self.functions.get("main_void"))

    def __interpret(self, node):

        node_type = node.__class__.__name__
        if self.debug > 0:
            print node_type

        if node_type == "ArithmeticNode":
            self.__arithmetic(node)
        elif node_type == "AssignNode":
            self.__assign(node)
        elif node_type == "BoolNode":
            self.__bool(node)
        elif node_type == "CallNode":
            self.__call(node)
        elif node_type == "CompoundNode":
            self.__compound(node)
        elif node_type == "ConditionNode":
            self.__condition(node)
        elif node_type == "FunctionNode":
            self.__function(node)
        elif node_type == "IfNode":
            self.__if(node)
        elif node_type == "IndexNode":
            self.__index(node)
        elif node_type == "IntNode":
            self.__int(node)
        elif node_type == "LogicNode":
            self.__logic(node)
        elif node_type == "NewVariableNode":
            self.__new_variable(node)
        elif node_type == "NotNode":
            self.__not(node)
        elif node_type == "ParamsNode":
            self.__params(node)
        elif node_type == "ReturnNode":
            self.__return(node)
        elif node_type == "StatementsNode":
            self.__statements(node)
        elif node_type == "VariableNode":
            self.__variable(node)
        elif node_type == "WhileNode":
            self.__while(node)
        else:
            raise Exception(node_type + " is an unrecognized type")

    def __arithmetic(self, node):

        self.__interpret(node.get_left_expression())
        left = self.stack.pop()
        left = self.__get_int(left)

        self.__interpret(node.get_right_expression())
        right = self.stack.pop()
        right = self.__get_int(right)

        arithmetic = node.get_arithmetic_operation()

        if arithmetic == "+":
            self.stack.append(left + right)
        elif arithmetic == "-":
            self.stack.append(left - right)
        elif arithmetic == "*":
            self.stack.append(left * right)
        elif arithmetic == "/":
            self.stack.append(left / right)
        elif arithmetic == "%":
            self.stack.append(left % right)
        else:
            raise Exception("Unrecognized arithmetic operation")

    def __assign(self, node):
        self.__interpret(node.get_left())
        variable_box = self.stack.pop()

        self.__interpret(node.get_right())
        value_box = self.stack.pop()

        self.__assign_box(variable_box, value_box)

        self.stack.append(variable_box)

    def __assign_box(self, variable_box, value_box):
        value = self.__typecast(variable_box, value_box)
        variable_box.set_value(value)

    def __typecast(self, variable_box, value_box):
        if isinstance(variable_box, IntBox):
            return self.__typecast_int(value_box)
        elif isinstance(variable_box, BoolBox):
            return self.__typecast_bool(value_box)
        elif isinstance(variable_box, ArrayBox):
            if self.__type_str(variable_box) == self.__type_str(value_box):
                return value_box
            else:
                raise Exception("Unable to typecast to correct array type")
        else:
            raise Exception("Unrecognized type")

    @staticmethod
    def __typecast_bool(value):
        if isinstance(value, ArrayBox):
            return True
        elif isinstance(value, (int, bool)):
            return bool(value)
        elif isinstance(value, (IntBox, BoolBox)):
            return bool(value.get_value())
        else:
            raise Exception("Unable to typecast into boolean")

    @staticmethod
    def __typecast_int(value):
        if isinstance(value, (int, bool)):
            return int(value)
        elif isinstance(value, (IntBox, BoolBox)):
            return int(value.get_value())
        else:
            raise Exception("Unable to typecast into int")

    @staticmethod
    def __typecast_array(value, variable):

        if not isinstance(value, ArrayBox):
            raise Exception("Excepted array type")

        if value.get_size() != variable.get_size():
            raise Exception("Incorrect array size")

        return value

    def __bool(self, node):
        self.stack.append(node.get_value())

    def __built_in_functions(self, node):
        func = self.built_in_functions_map.get(node.get_function_name().get_value())
        if func is None:
            raise Exception("Code for built in function not written")

        func(node.get_params())

    def __print(self, params):
        for param in params:
            self.__interpret(param)
            print self.stack.pop()

    def __read(self, params):

        for i in range(len(params)):

            self.__interpret(params[i])
            param_box = self.stack.pop()
            if not isinstance(param_box, Box):
                raise Exception("Can only read into variable")

            self.__read_box(param_box)

    def __read_box(self, param_box):

        if isinstance(param_box, IntBox):
            self.__read_int(param_box)
        elif isinstance(param_box, BoolBox):
            self.__read_bool(param_box)
        elif isinstance(param_box, ArrayBox):
            self.__read_array(param_box)
        else:
            raise Exception("Cannot read void type")

    @staticmethod
    def __ignore_spaces():
        c = sys.stdin.read(1)
        while c.isspace() or c == '':
            c = sys.stdin.read(1)
        return c

    def __read_int(self, var_box):
        var_box.set_value(int(self.__read_word()))

    def __read_bool(self, var_box):
        var_box.set_value(bool(self.__read_word()))

    def __read_word(self):
        c = self.__ignore_spaces()

        value = ""
        while not c.isspace():
            if c != '':
                value += c
            c = sys.stdin.read(1)

        return value

    def __read_array(self, var_box):
        for box in var_box:
            self.__read_box(box)

    def __call(self, node):

        function_name = node.get_function_name().get_value()
        if function_name in self.built_in_functions:
            self.__built_in_functions(node)
            return

        interpreted_params = []
        for param in node.get_params():
            self.__interpret(param)
            interpreted_params.append(self.stack.pop())
            function_name += "_" + self.__type_str(interpreted_params[-1])

        function = self.functions.get(function_name)
        if function is None:
            raise Exception("Could not match function of type " + function_name)

        self.env = Environment()
        self.environments.append(self.env)

        # self.__interpret(function.get_params())
        self.__set_params(function.get_params().get_params(), interpreted_params)

        # run function
        self.__interpret(function)

        self.environments.pop()
        self.env = self.environments[-1]

        # check if top of stack is return statement(r)
        if len(self.stack) != 0 and isinstance(self.stack[-1], ReturnStatement):
            return_val = self.stack.pop().args[0]

            # typecast
            if isinstance(function.get_return_type(), VoidType):
                if return_val is not None:
                    raise Exception("Incorrect return type")
            elif isinstance(function.get_return_type(), IntType):
                if not isinstance(return_val, (int, IntBox)):
                    raise Exception("Incorrect return type")
            elif isinstance(function.get_return_type(), BoolType):
                if not isinstance(return_val, (BoolBox, bool)):
                    raise Exception("Incorrect return type")
            elif isinstance(function.get_return_type(), ArrayType):
                if not isinstance(return_val, ArrayBox):
                    raise Exception("Incorrect return type")

            self.stack.append(return_val)
        else:
            if str(function.get_return_type()) != "void":
                raise Exception("Missing return statement")

    def __type_str(self, value):
        if isinstance(value, (int, IntBox)):
            return "int"
        elif isinstance(value, (bool, BoolBox)):
            return "bool"
        elif isinstance(value, ArrayBox):
            return "array_" + self.__type_str(value.get_value(0))
        else:
            raise Exception("Unrecognized type")

    def __set_params(self, params, param_exprs):
        for i in range(len(params)):
            param_expr = param_exprs[i]
            param_var = params[i].get_variable_name()
            self.__interpret(params[i])
            self.__interpret(param_var)
            variable_box = self.stack.pop()
            self.__assign_box(variable_box, param_expr)

    def __compound(self, node):
        self.env.new_scope()
        self.__interpret(node.get_statements())

    def __condition(self, node):
        self.__interpret(node.get_left_expression())
        left = self.stack.pop()
        left = self.__get_int(left)

        self.__interpret(node.get_right_expression())
        right = self.stack.pop()
        right = self.__get_int(right)

        comparison = node.get_comparison()

        if comparison == "<":
            self.stack.append(left < right)
        elif comparison == "<=":
            self.stack.append(left <= right)
        elif comparison == ">=":
            self.stack.append(left >= right)
        elif comparison == ">":
            self.stack.append(left > right)
        elif comparison == "!=":
            self.stack.append(left != right)
        elif comparison == "==":
            self.stack.append(left == right)
        else:
            raise Exception("Unrecognized comparison operation")

    def __function(self, node):
        self.function_locs.append(len(self.stack))

        try:
            self.__interpret(node.get_statements())
        except ReturnStatement as r:
            loc = self.function_locs.pop()
            self.stack = self.stack[:loc]
            self.stack.append(r)

    def __if(self, node):

        self.__interpret(node.get_condition())
        conditional = self.stack.pop()
        conditional = self.__get_bool(conditional)

        if conditional:
            self.__interpret(node.get_true_expression())
        else:
            false_expr = node.get_false_expression()
            if false_expr is not None:
                self.__interpret(node.get_false_expression())

    def __index(self, node):
        self.__interpret(node.get_name())
        array_box = self.stack.pop()
        array_box = self.__get_array(array_box)

        self.__interpret(node.get_index())
        value = self.stack.pop()
        value = self.__get_int(value)

        self.stack.append(array_box.get_value(value))

    def __int(self, node):
        self.stack.append(node.get_value())

    def __logic(self, node):
        self.__interpret(node.get_left_expression())
        left = self.stack.pop()
        left = self.__get_int(left)

        logic = node.get_logic_operation()

        # short circuit operations
        if logic == "&&" and left is False:
            self.stack.append(False)
            return

        if logic == "||" and left is True:
            self.stack.append(True)
            return

        self.__interpret(node.get_right_expression())
        right = self.stack.pop()
        right = self.__get_int(right)

        if logic == "&&":
            self.stack.append(left and right)
        elif logic == "||":
            self.stack.append(left or right)
        else:
            raise Exception("Unrecognized logical operation")

    def __new_variable(self, node):
        node_type = node.get_type()
        variable_name = node.get_variable_name().get_value()

        if node_type.__class__.__name__ == "ArrayType":
            self.__interpret(node_type.get_size())
            box = self.stack.pop()
            box = self.__get_int(box)
            node_type.set_size(box)

        self.env.add_variable(variable_name, node_type)

    def __not(self, node):

        self.__interpret(node.get_expression())
        value = self.stack.pop()
        self.stack.append(not self.__get_bool(value))

    @staticmethod
    def __get_int(value):
        if isinstance(value, IntBox):
            return value.get_value()
        elif not isinstance(value, int):
            raise Exception("Expected type int")
        return value

    @staticmethod
    def __get_bool(value):
        if isinstance(value, BoolBox):
            return value.get_value()
        elif not isinstance(value, bool):
            raise Exception("Expected type bool")
        return value

    @staticmethod
    def __get_array(value):
        if isinstance(value, ArrayBox):
            return value
        raise Exception("Expected type array")

    def __params(self, node):
        for param in node.get_params():
            self.__interpret(param)

    def __return(self, node):
        if node.get_return_value() is None:
            raise ReturnStatement(None)
        else:
            self.__interpret(node.get_return_value())
            raise ReturnStatement(self.stack.pop())

    def __statements(self, node):
        for statement in node.get_statements():
            self.__interpret(statement)

            statement_type = statement.__class__.__name__
            if statement_type not in ("IfNode", "WhileNode", "ReturnNode", "NewVariableNode", "CallNode"):
                self.stack.pop()

    def __variable(self, node):
        variable_name = node.get_value()
        self.stack.append(self.env.get_variable(variable_name))

    def __while(self, node):
        condition = node.get_condition()
        expression = node.get_expression()

        self.__interpret(condition)
        conditional_value = self.stack.pop()
        conditional_value = self.__get_bool(conditional_value)
        while conditional_value:
            self.__interpret(expression)
            self.__interpret(condition)
            conditional_value = self.stack.pop()
            conditional_value = self.__get_bool(conditional_value)
