from abc import ABCMeta, abstractmethod


class Box():
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_value(self):
        pass

    @abstractmethod
    def get_value(self):
        pass
