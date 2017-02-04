from node import Node

class FunctionNode(Node):

    def __init__(self, name, params, statements, return_type):
        self.name = name
        self.params = params
        self.statements = statements
        self.return_type = return_type

    def get_function_name(self):
        return self.name.get_value()

    def get_function_name_with_params(self):
        return self.name.get_value() + str(self.params)

    def get_return_type(self):
        return self.return_type

    def get_statements(self):
        return self.statements

    def get_params(self):
        return self.params