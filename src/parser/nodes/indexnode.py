from node import Node

class IndexNode(Node):
    def __init__(self, variable, index):
        self.variable = variable
        self.index = index
        self.type = None

    def set_type(self, new_type):
        if self.type is None:
            raise Exception("Already typed")

        self.type = new_type

    def get_name(self):
        return self.variable

    def get_index(self):
        return self.index