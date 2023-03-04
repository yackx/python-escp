from enum import Enum


class Typeface(Enum):
    ROMAN = 0
    SANS_SERIF = 1


class Margin(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class PageLengthUnit(Enum):
    LINES = 0
    INCHES = 1
