class AutoCounter:

    def __init__(self, start_value = 0):
        self._value = start_value

    @property
    def next(self):
        next_value = self._value
        self._value += 1
        return next_value

class Counter:

    def __init__(self, start_value = 0):
        self._value = 0

    def increment(self):
        self._value += 1

    @property
    def value(self):
        return self.__value
