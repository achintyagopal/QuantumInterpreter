from abc import ABCMeta, abstractmethod
import sys

from ast.types.voidtype import VoidType
from ast.types.inttype import IntType
from ast.types.booltype import BoolType
from ast.types.arraytype import ArrayType
from ast.nodes.assignnode import AssignNode
from ast.nodes.statementsnode import StatementsNode

class Box():
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_value(self):
        pass

    @abstractmethod
    def get_value(self):
        pass

class IntBox(Box):
    def __init__(self):
        self.value = 0

    def set_value(self, value):
        self.value = int(value)

    def get_value(self):
        return self.value

    def __str__(self):
        return str(self.value)


class BoolBox(Box):
    def __init__(self):
        self.value = False

    def set_value(self, value):
        self.value = bool(value)

    def get_value(self):
        return self.value

    def __str__(self):
        return str(self.value)


class ArrayBox(Box):

    def __init__(self, type, size):
        self.values = []
        for _ in range(size):
            if type.__class__.__name__ == "IntType":
                self.values.append(IntBox())
            elif type.__class__.__name__ == "BoolType":
                self.values.append(BoolBox())
            else:
                raise Exception("Could not create array box")

    def set_value(self, array_box):
        self.values = array_box.values

    def get_value(self, index):
        return self.values[index]

    def __str__(self):
        string = "["
        i = 0
        for value in self.values:
            if i == 0:
                string += value
            else:
                string += ", " + str(value)
        string += "]"
        return string

    def __iter__(self):
        return iter(self.values)


class Scope():
    def __init__(self, old_scope = None):
        self.variables = {}
        self.previous = old_scope

    def add_variable(self, name, variable_type):
        if self.variables.get(name) is not None:
            raise Exception("Variable of name " + name + " already exists")

        if variable_type.__class__.__name__ == "IntType":
            self.variables[name] = IntBox()
        elif variable_type.__class__.__name__ == "BoolType":
            self.variables[name] = BoolBox()
        elif variable_type.__class__.__name__ == "ArrayType":
            self.variables[name] = ArrayBox(variable_type.get_type(), variable_type.get_size())
        else:
            raise Exception("Invalid type")

    def get_variable(self, variable_name):

        box = self.variables.get(variable_name)
        if box is not None:
            return box

        if self.previous is not None:
            return self.previous.get_variable(variable_name)
        else:
            raise Exception("Variable " + variable_name + " does not exist")

    def previous_scope(self):
        return self.previous


class Environment():
    def __init__(self):
        self.current_scope = Scope()

    def new_scope(self):
        self.current_scope = Scope(self.current_scope)

    def remove_scope(self):
        self.current_scope = self.current_scope.previous_scope()

    def add_variable(self, variable_name, variable_type):
        self.current_scope.add_variable(variable_name, variable_type)

    def get_variable(self, variable_name):
        return self.current_scope.get_variable(variable_name)


class ReturnStatement(Exception):
    pass


class Interpreter():
    def __init__(self, ast, debug=0):
        self.ast = ast
        self.functions = {}
        self.stack = []
        self.env = Environment()
        self.function_locs = []
        self.debug = debug
        self.built_in_functions = ("print", "read")

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
        left = self.__typecast_int(left)

        self.__interpret(node.get_right_expression())
        right = self.stack.pop()
        right = self.__typecast_int(right)

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

        if isinstance(variable_box, (IntBox, BoolBox)):
            if isinstance(value_box, (IntBox, BoolBox)):
                variable_box.set_value(value_box.get_value())
            elif isinstance(value_box, (int, bool)):
                variable_box.set_value(value_box)
            else:
                raise Exception("Can only assign an int or bool")
        elif isinstance(variable_box, ArrayBox):
            if isinstance(value_box, ArrayBox):
                variable_box.set_value(value_box)
            else:
                raise Exception("Mismatch types")
        else:
            raise Exception("Can only assign to int or bool variable")

        self.stack.append(variable_box)

    def __bool(self, node):
        self.stack.append(node.get_value())

    def __built_in_functions(self, node):
        if node.get_function_name().get_value() == "print":
            self.__print(node.get_params())
        elif node.get_function_name().get_value() == "read":
            self.__read(node.get_params())
        else:
            raise Exception("Code for built in function not written")

    def __print(self, params):
        for param in params:
            self.__interpret(param)
            print self.stack.pop()

    def __read(self, params):

        for i in range(len(params)):
            # param_var = params[i].get_variable_name()
            # param_type = params[i].get_type()

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

        # find which function
        function_keys = []
        function_name = node.get_function_name().get_value()
        if function_name in self.built_in_functions:
            self.__built_in_functions(node)
            return

        for key, value in self.functions.iteritems():

            if key == function_name:
                function_keys.append(value)

        if len(function_keys) == 0:
            raise Exception("Function " + function_name + " does not exist")
        elif len(function_keys) == 1:
            function = function_keys[0]
        else:
            new_function_keys = []
            for fn in function_keys:
                if fn.get_params().get_size() == node.get_params().get_size():
                    new_function_keys.append(fn)

            if len(new_function_keys) == 1:
                function = new_function_keys[0]
            else:
                raise Exception("Could not resolve function")

        self.env.new_scope()

        # create new variable nodes
        self.__interpret(function.get_params())

        # assign each node
        self.__set_params(function.get_params(), node.get_params())

        # run function
        self.__interpret(function)

        # check if top of stack is return statement(r)
        if isinstance(self.stack[-1], ReturnStatement):
            return_val = self.stack.pop().message

            # typecast
            if isinstance(function.get_return_type(), VoidType):
                if return_val is None:
                    value = None
                else:
                    raise Exception("Incorrect return type")

            elif isinstance(function.get_return_type(), IntType):
                value = self.__typecast_int(return_val)
            elif isinstance(function.get_return_type(), BoolType):
                value = self.__typecast_bool(return_val)
            elif isinstance(function.get_return_type(), ArrayType):
                value = self.__typecast_array(return_val)

            self.stack.append(value)
        else:
            if str(function.get_return_type()) != "void":
                raise Exception("Missing return statement")

    def __set_params(self, params, param_exprs):
        statements = []
        for i in range(len(params)):
            param_expr = param_exprs[i]
            param_var = params[i].get_variable_name()
            statements.append(AssignNode(param_var, param_expr))
        statements = StatementsNode(statements)
        self.__interpret(statements)

    def __compound(self, node):
        self.env.new_scope()
        self.__interpret(node.get_statements())

    def __condition(self, node):
        self.__interpret(node.get_left_expression())
        left = self.stack.pop()
        left = self.__typecast_int(left)

        self.__interpret(node.get_right_expression())
        right = self.stack.pop()
        right = self.__typecast_int(right)

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
            self.stack.append(ReturnStatement(r))

    def __if(self, node):

        self.__interpret(node.get_condition())
        conditional = self.stack.pop()

        condition_value = self.__typecast_bool(conditional)

        if condition_value:
            self.__interpret(node.get_true_expression())
        else:
            self.__interpret(node.get_false_expression())

    def __index(self, node):
        self.__interpret(node.get_name())
        array_box = self.stack.pop()

        self.__interpret(node.get_index())
        value = self.stack.pop()

        value = self.__typecast_int(value)
        array_box = self.__typecast_array(array_box)
        self.stack.append(array_box.get_value(int(value)))

    def __int(self, node):
        self.stack.append(node.get_value())

    def __logic(self, node):
        self.__interpret(node.get_left_expression())
        left = self.stack.pop()
        left = self.__typecast_int(left)

        logic = node.get_logic_operation()

        # short circuit operations
        if logic == "&&" and left == False:
            self.stack.append(False)
            return

        if logic == "||" and left == True:
            self.stack.append(True)
            return

        self.__interpret(node.get_right_expression())
        right = self.stack.pop()
        right = self.__typecast_int(right)

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
            if isinstance(BoolBox, IntBox):
                node_type.set_size(box.get_value())
            elif isinstance(int, bool):
                node_type.set_size(box.get_value())
            else:
                raise Exception("Cannot create array of non-int size")

        self.env.add_variable(variable_name, node_type)

    def __not(self, node):

        self.__interpret(node.get_expression())
        value = self.stack.pop()
        self.stack.append(not self.__typecast_bool(value))

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
    def __typecast_array(value):

        if not isinstance(value, ArrayBox):
            raise Exception("Excepted array type")

        return value

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
        while conditional_value:
            self.__interpret(expression)
            self.__interpret(condition)
            conditional_value = self.stack.pop()
