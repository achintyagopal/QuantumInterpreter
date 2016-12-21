from node import Node

class ReturnNode(Node):

    def __init__(self, return_value):

        if isinstance(return_value, list):
            self.return_value = return_value

        self.return_value = return_value
