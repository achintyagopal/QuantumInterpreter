from node import Node

class ConditionNode(Node):

    def __init__(self, comparison, expression1, expression2):
        self.comparison = comparison
        self.expression_l = expression1
        self.expression_r = expression2

    def get_left_expression(self):
        return self.expression_l

    def get_right_expression(self):
        return self.expression_r

    def get_comparison(self):
        return self.comparison