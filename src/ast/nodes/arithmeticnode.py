from node import Node

class ArithmeticNode(Node):

    def __init__(self, arithmetic, expression1, expression2):
        self.arithmetic = arithmetic
        self.expression_l = expression1
        self.expression_r = expression2
