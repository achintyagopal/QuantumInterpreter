from node import Node

class IfNode(Node):

    def __init__(self, condition, true_expr, false_expr = None):

        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr
