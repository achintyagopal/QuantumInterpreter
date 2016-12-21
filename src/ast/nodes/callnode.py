from node import Node

class CallNode(Node):

    def __init__(self, function_name, params):
        self.function_name = function_name
        self.params = params
