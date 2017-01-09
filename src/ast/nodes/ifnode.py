from node import Node

class IfNode(Node):

    def __init__(self, condition, true_expr, false_expr = None):

        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def get_condition(self):
        return self.condition

    def get_true_expression(self):
        return self.true_expr

    def get_false_expression(self):
        return self.false_expr