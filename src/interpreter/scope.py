from box.intbox import IntBox
from box.boolbox import BoolBox
from box.arraybox import ArrayBox


class Scope():
    def __init__(self, old_scope = None):
        self.variables = {}
        self.previous = old_scope

    def add_variable(self, name, variable_type):
        if self.variables.get(name) is not None:
            raise Exception("Variable of name " + name + " already exists")

        if variable_type.__class__.__name__ == "IntType":
            self.variables[name] = IntBox()
        elif variable_type.__class__.__name__ == "BoolType":
            self.variables[name] = BoolBox()
        elif variable_type.__class__.__name__ == "ArrayType":
            self.variables[name] = ArrayBox(variable_type.get_type(), variable_type.get_size())
        else:
            raise Exception("Invalid type")

    def get_variable(self, variable_name):

        box = self.variables.get(variable_name)
        if box is not None:
            return box

        if self.previous is not None:
            return self.previous.get_variable(variable_name)
        else:
            raise Exception("Variable " + variable_name + " does not exist")

    def previous_scope(self):
        return self.previous