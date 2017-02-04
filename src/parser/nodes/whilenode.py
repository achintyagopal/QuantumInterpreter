from node import Node

class WhileNode(Node):

    def __init__(self, condition, expression):

        self.condition = condition
        self.expression = expression

    def get_condition(self):
        return self.condition

    def get_expression(self):
        return self.expression