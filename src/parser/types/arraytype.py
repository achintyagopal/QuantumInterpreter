from Type import Type

class ArrayType(Type):
    def __init__(self, type, expression):
        self.type = type
        self.expression = expression

    def __str__(self):
        return "array_" + str(self.type)

    def get_size(self):
        return self.expression

    def get_type(self):
        return self.type

    def set_size(self, size):
        self.expression = int(size)