from node import Node

class CompoundNode(Node):

    def __init__(self, statements):
        self.statements = statements

    def get_statements(self):
        return self.statements