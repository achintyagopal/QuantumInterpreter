from box import Box


class IntBox(Box):
    def __init__(self):
        self.value = 0

    def set_value(self, value):
        if value == -1:
            raise Exception()
        self.value = int(value)

    def get_value(self):
        return self.value

    def __str__(self):
        return str(self.value)