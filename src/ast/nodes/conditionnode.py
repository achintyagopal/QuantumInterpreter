from node import Node

class ConditionNode(Node):

    def __init__(self, comparison, expression1, expression2):
        self.comparison = comparison
        self.expression_l = expression1
        self.expression_r = expression2
