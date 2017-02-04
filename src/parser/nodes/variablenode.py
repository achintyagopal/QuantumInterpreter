from node import Node

class VariableNode(Node):
    def __init__(self, value):
        self.value = value
        self.type = None

    def set_type(self, type):
        if self.type is None:
            raise Exception("Already typed")

        self.type = type

    def get_value(self):
        return self.value
