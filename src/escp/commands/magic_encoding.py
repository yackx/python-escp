from .parameters import CharacterSetVariant


# International character set [R-41]
# Very basic table, far from complete
magic_encoding = {
    "#": (CharacterSetVariant.USA, b'\x23'),
    "$": (CharacterSetVariant.USA, b'\x24'),
    "@": (CharacterSetVariant.USA, b'\x40'),
    "[": (CharacterSetVariant.USA, b'\x5b'),
    "\\": (CharacterSetVariant.USA, b'\x5c'),
    "]": (CharacterSetVariant.USA, b'\x5d'),
    "^": (CharacterSetVariant.USA, b'\x5e'),
    "`": (CharacterSetVariant.USA, b'\x60'),
    "{": (CharacterSetVariant.USA, b'\x7b'),
    "|": (CharacterSetVariant.USA, b'\x7c'),
    "}": (CharacterSetVariant.USA, b'\x7d'),
    "˜": (CharacterSetVariant.USA, b'\x7e'),
    "à": (CharacterSetVariant.FRANCE, b'\x40'),
    "°": (CharacterSetVariant.FRANCE, b'\x5b'),
    "ç": (CharacterSetVariant.FRANCE, b'\x5c'),
    "§": (CharacterSetVariant.FRANCE, b'\x5d'),
    "é": (CharacterSetVariant.FRANCE, b'\x7b'),
    "ù": (CharacterSetVariant.FRANCE, b'\x7c'),
    "è": (CharacterSetVariant.FRANCE, b'\x7d'),
    "¨": (CharacterSetVariant.FRANCE, b'\x7e'),
    "©": (CharacterSetVariant.LEGAL, b'\x7b'),
    "®": (CharacterSetVariant.LEGAL, b'\x7c'),
}
