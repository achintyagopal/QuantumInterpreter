from node import Node

class ParamsNode(Node):

    def __init__(self, param_list):
        self.param_list = param_list

    def __str__(self):
        param_str = ""
        if not self.param_list:
            return "_void"

        for param in self.param_list:
            param_str += "_" + str(param.type)
        return param_str

    def get_params():
        return self.param_list

    def get_size():
        return len(self.param_list)