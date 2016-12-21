from node import Node

class WhileNode(Node):

    def __init__(self, condition, expression):

        self.condition = condition
        self.expression = expression
