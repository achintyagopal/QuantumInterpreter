from node import Node

class CallNode(Node):

    def __init__(self, function_name, params):
        self.function_name = function_name
        self.params = params

    def get_function_name(self):
        return self.function_name

    def get_params(self):
        return self.params