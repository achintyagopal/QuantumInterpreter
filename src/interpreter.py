class IntBox():

    def __init__(self):
        self.value = 0

    def set_value(self, value):
        self.value = int(value)

    def get_value(self):
        return self.value


class BoolBox():

    def __init__(self):
        self.value = False

    def set_value(self, value):
        self.value = bool(value)

    def get_value(self):
        return self.value


class ArrayBox():

    def __init__(self, type, size):
        self.values= []
        for _ in range(size):
            if type.__class__.__name__ == "IntType":
                self.values.append(IntBox())
            elif type.__class__.__name__ == "BoolType":
                self.values.append(BoolBox())
            else:
                raise Exception("Could not create array box")

    def set_value(self, index, value):
        self.values[index].set_value(value)

    def get_value(self, index):
        return self.values[index].get_value()


class Scope():

    def __init__(self, old_scope):
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


class Environment():

    def __init__(self):
        self.current_scope = None

    def new_scope(self):
        self.current_scope = Scope(self.current_scope)

    def add_variable(self, variable_name, variable_type):
        self.current_scope.add_variable(variable_name, variable_type)

    def get_variable(self, variable_name):
        return self.current_scope.get_variable(variable_name)

class Interpreter():

    def __init__(self, ast):
        self.ast = ast
        self.functions = {}
        self.stack = []
        self.env = Environment()
        self.function_locs = []

    def interpret(self):

        for function in self.ast.program:
            function_name = function.get_function_name()
            return_type = function.get_return_type()

            if self.functions.get(function_name) is not None:
                raise Exception(function_name + " already exists")

            self.functions[function_name] = function

        if self.functions.get("main_void") is None:
            return

        self.__interpret(self.functions.get("main_void"))

    def __interpret(self, node):

        node_type = node.__class__.__name__
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
        pass

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

        else:
            raise Exception("Can only assign to int or bool variable")

        self.stack.append(variable_box)

    def __bool(self, node):
        self.stack.append(node.get_value())

    # TODO
    def __call(self, node):
        pass

    def __compound(self, node):
        self.env.new_scope()
        self.__interpret(node.statements)

    # TODO
    def __condition(self, node):
        pass

    # TODO
    def __function(self, node):
        self.function_locs.append(len(self.stack))
        self.env.new_scope()
        self.__interpret(node.get_statements())

    # TODO
    def __if(self, node):
        pass

    def __index(self, node):
        self.__interpret(node.get_name())
        array_box = self.stack.pop()

        self.__interpret(node.get_index())
        value = self.stack.pop()

        if isinstance(value, (IntBox, BoolBox)):
            value = value.get_value()
        elif not isinstance(value, (int, bool)):
            raise Exception("Can only index with index or bool")

        if isinstance(array_box, ArrayBox):
            array_box.get_value(int(value))
        else:
            raise Exception("Can only index an array")

    def __int(self, node):
        self.stack.append(node.get_value())

    # TODO
    def __logic(self, node):
        pass

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

    # TODO
    def __not(self, node):
        pass

    # TODO
    def __params(self, node):
        pass

    # TODO
    def __return(self, node):
        pass

    def __statements(self, node):
        for statement in node.get_statements():
            self.__interpret(statement)

            statement_type = statement.__class__.__name__
            if statement_type not in ("IfNode", "WhileNode", "ReturnNode", "NewVariableNode"):
                self.stack.pop()

    def __variable(self, node):
        variable_name = node.get_value()
        self.stack.append(self.env.get_variable(variable_name))

    # TODO
    def __while(self, node):
        pass
