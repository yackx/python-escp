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


class Justification(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    FULL = 3


class CharacterSetVariant(Enum):
    USA = 0
    FRANCE = 1
    GERMANY = 2
    UK = 3
    DENMARK_I = 4
    SWEDEN = 5
    ITALY = 6
    SPAIN_I = 7
    JAPAN = 8
    NORWAY = 9
    DENMARK_II = 10
    SPAIN_II = 11
    LATIN_AMERICA = 12
    KOREA = 13
    LEGAL = 64