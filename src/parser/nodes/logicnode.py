from node import Node

class LogicNode(Node):

    def __init__(self, logic, expression1, expression2):
        self.logic = logic
        self.expression_l = expression1
        self.expression_r = expression2

    def get_logic_operation(self):
        return self.logic

    def get_left_expression(self):
        return self.expression_l

    def get_right_expression(self):
        return self.expression_r
