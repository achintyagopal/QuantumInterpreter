from box import Box
from intbox import IntBox
from boolbox import BoolBox


class ArrayBox(Box):

    def __init__(self, type, size):

        if size <= 0:
            raise Exception("Cannot initialize array of size " + str(size))

        self.values = []
        for _ in range(size):
            if type.__class__.__name__ == "IntType":
                self.values.append(IntBox())
            elif type.__class__.__name__ == "BoolType":
                self.values.append(BoolBox())
            else:
                raise Exception("Could not create array box")

    def set_value(self, array_box):
        self.values = array_box.values

    def get_value(self, index):
        return self.values[index]

    def get_size(self):
        return len(self.values)

    def __str__(self):
        string = "["
        i = 0
        for value in self.values:
            if i == 0:
                string += value
            else:
                string += ", " + str(value)
        string += "]"
        return string

    def __iter__(self):
        return iter(self.values)
