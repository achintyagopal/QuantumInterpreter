from box import Box


class BoolBox(Box):
    def __init__(self):
        self.value = False

    def set_value(self, value):
        self.value = bool(value)

    def get_value(self):
        return self.value

    def __str__(self):
        return str(self.value)