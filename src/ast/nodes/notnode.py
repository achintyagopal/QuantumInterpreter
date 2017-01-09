from node import Node

class NotNode(Node):

    def __init__(self, expression):
        self.expression = expression

    def get_expression(self):
        return self.expression