from node import Node
from ..types.inttype import IntType

class IntNode(Node):
    def __init__(self, value):
        self.value = int(value)
        self.type = IntType()

    def get_value(self):
        return self.value