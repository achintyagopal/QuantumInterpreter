from node import Node

class ArithmeticNode(Node):

    def __init__(self, arithmetic, expression1, expression2):
        self.arithmetic = arithmetic
        self.expression_l = expression1
        self.expression_r = expression2

    def get_arithmetic_operation(self):
        return self.arithmetic

    def get_left_expression(self):
        return self.expression_l

    def get_right_expression(self):
        return self.expression_r