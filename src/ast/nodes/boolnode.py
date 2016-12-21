from ..types.booltype import BoolType
from node import Node

class BoolNode(Node):
    def __init__(self, value):
        self.value = bool(value)
        self.type = BoolType()

    def get_value(self):
        return self.value