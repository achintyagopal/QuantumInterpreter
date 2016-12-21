from node import Node

class LogicNode(Node):

    def __init__(self, logic, expression1, expression2):
        self.logic = logic
        self.expression_l = expression1
        self.expression_r = expression2
