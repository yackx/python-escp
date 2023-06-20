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


class CharacterTable(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, d2, d3):
        self.d2 = d2
        self.d3 = d3

    def __str__(self):
        return f'{self.name} (d2={self.d2}, d3={self.d3})'

    # int value is d2 and d3 parameters in the manual
    # d1 to be set separately
    # [C-75]

    ITALIC = 0, 0
    PC437_US = 1, 0
    PC437_GREEK = 1, 16
    PC932_JAPANESE = 2, 0
    PC850_MULTILINGUAL = 3, 0
    PC851_GREEK = 4, 0
    PC853_TURKISH = 5, 0
    PC855_CYRILLIC = 6, 0
    PC860_PORTUGAL = 7, 0
    PC863_CANADA_FRENCH = 8, 0
    PC865_NORWAY = 9, 0
    PC852_EAST_EUROPE = 10, 0
    PC857_TURKISH = 11, 0
    PC862_HEBREW = 12, 0
    PC864_ARABIC = 13, 0
    PC_AR864 = 13, 32
    PC866_RUSSIAN = 14, 0
    BULGARIAN_ASCII = 14, 16
    PC866_LAT_LATVIAN = 14, 32
    PC869_GREEK = 15, 0
    USSR_GOST_RUSSIAN = 16, 0
    ECMA_94_1 = 17, 0
    KU42_KU_THAI = 18, 0
    TIS11_TS_988_THAI = 19, 0
    TIS18_GENERAL_THAI = 20, 0
    TIS17_SIC_STD_T21HAI = 21, 0
    TIS13_IBM_STD_T22HAI = 22, 0
    TIS16_SIC_OLD_THAI = 23, 0
    PC861_ICELAND = 24, 0
    BRASCII = 25, 0
    ABICOMP = 26, 0
    MAZOWIA_POLAND = 27, 0
    CODE_MJK_CSFR = 28, 0
    ISO8859_7_LATIN_GREEK = 29, 7
    ISO8859_1_LATIN_1 = 29, 16
    TSM_WIN_THAI_SYSTEM_MANAGER = 30, 0
    ISO_LATIN_1T_TURKISH = 31, 0
    BULGARIA = 32, 0
    HEBREW_7 = 33, 0
    HEBREW_8 = 34, 0
    ROMAN_ = 35, 0
    PC_LITHUANIA = 36, 0
    ESTONIA_ESTONIA = 37, 0
    ISCII = 38, 0
    PC_ISCII = 39, 0
    PC_APTEC = 40, 0
    PC = 41, 0
    PC720 = 42, 0
    OCR_B = 112, 0
    ISO_LATIN_1 = 127, 1
    ISO_8859_2_LATIN_2 = 127, 2
    ISO_LATIN_7_GREEK = 127, 7,
