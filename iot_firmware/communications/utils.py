"""Utils for the communications package."""


class Counter:
    """Counter that sums a value every time it is called.

    :param start: starting counter value
    :param increment: increment value of the counter

    Basic usage.

    >>> counter = Counter()
    >>> counter()
    1
    >>> counter()
    2

    Supports starting the counter at a specific value.

    >>> counter = Counter(start=10)
    >>> counter()
    11

    Supports modifying the increment value after each call.

    >>> counter = Counter(increment=5)
    >>> counter()
    5
    """

    def __init__(self, start: int = 0, increment: int = 1) -> None:
        self.__value = start
        self.__increment = increment

    def __call__(self) -> int:
        self.__value += self.__increment
        return self.__value
