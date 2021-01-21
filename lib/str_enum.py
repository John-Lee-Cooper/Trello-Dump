""" StrEnum class """

from enum import Enum
from typing import Optional


class StrEnum(str, Enum):
    """
    A string enum class that
      * adds an integer index to each enum
      * returns the string value for str()

    (python -m doctest <module>)

    >>> class Pie(StrEnum):
    ...    APPLE = "Apple"
    ...    PECAN = "Pecan"
    ...    BLUE_BERRY = "Blue Berry"

    >>> Pie
    <enum 'Pie'>

    >>> ", ".join(Pie)
    'Apple, Pecan, Blue Berry'


    # access by index
    >>> Pie.get(1)
    <Pie.APPLE: 'Apple'>

    >>> int(Pie.get(2))
    2

    # access by name and value
    >>> Pie.BLUE_BERRY is Pie('Blue Berry')
    True

    >>> pie = Pie.PECAN

    >>> pie.name
    'PECAN'

    # repr
    >>> pie
    <Pie.PECAN: 'Pecan'>

    # str
    >>> pie.value, str(pie)
    ('Pecan', 'Pecan')

    """

    def __init__(self, value):
        self._index = len(self.__class__) + 1

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self._index

    @classmethod
    def get(cls, index, default=None) -> Optional["StrEnum"]:
        """ Return enum with index=index, else default """
        index -= 1
        for i, enum in enumerate(cls):
            if i == index:
                return enum
        return default
