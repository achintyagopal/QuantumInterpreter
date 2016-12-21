from node import Node

class AssignNode(Node):

    def __init__(self, expression1, expression2):
        self.expression_l = expression1
        self.expression_r = expression2

    def get_left(self):
        return self.expression_l

    def get_right(self):
        return self.expression_r