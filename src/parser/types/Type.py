class Type():
    def __eq__(self, other):
        try:
            if self.__class__.__name__ == other.__class__.name__:
                return True
        except:
            return False
        return False