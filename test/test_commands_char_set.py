import pytest
from escp.commands.parameters import CharacterSetVariant

from src.escp import Commands, Margin, PageLengthUnit, Typeface
from src.escp.commands.commands import T


class CommandsDefault(Commands):
    def line_spacing(self, numerator: int, denominator: int) -> T:
        raise NotImplementedError()


@pytest.fixture
def commands():
    return CommandsDefault()


def test_char_set(commands):
    assert commands.character_set(CharacterSetVariant.FRANCE).buffer == b'\x1bR\x01'


def test_char_brace(commands):
    assert commands.text("{", encoding='cp437').buffer == b'\x7b'


def test_char_e_accent(commands):
    assert commands.text("é", encoding='cp437').buffer == b'\x82'
