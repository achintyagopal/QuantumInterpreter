from node import Node

class NewVariableNode(Node):

    def __init__(self, variable_name, new_type):
        self.variable_name = variable_name
        self.type = new_type

    def get_type(self):
        return self.type

    def get_variable_name(self):
        return self.variable_name

