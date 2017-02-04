from scope import Scope


class Environment():
    def __init__(self):
        self.current_scope = Scope()

    def new_scope(self):
        self.current_scope = Scope(self.current_scope)

    def remove_scope(self):
        self.current_scope = self.current_scope.previous_scope()

    def add_variable(self, variable_name, variable_type):
        self.current_scope.add_variable(variable_name, variable_type)

    def get_variable(self, variable_name):
        return self.current_scope.get_variable(variable_name)
