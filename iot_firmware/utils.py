class Counter:
    def __init__(self, start: int = 0):
        self._value = start

    def __call__(self):
        self._value += 1
        return self._value
