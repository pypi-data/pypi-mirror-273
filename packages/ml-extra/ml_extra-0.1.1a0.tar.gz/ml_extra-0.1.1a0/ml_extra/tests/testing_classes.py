from ml_extra.loggers.decorators.code import log_class

from abc import ABC


@log_class
class DummyClass(ABC):

    def __init__(self):
        pass

    def say_something(self, something):
        print(something)


@log_class
class DummyClass2(ABC):

    def __init__(self):
        pass

    def say_something(self, something):
        print(something)

    def say_something_else(self, something):
        print(something)
