import pytest
from escp.commands.parameters import CharacterSetVariant

from test import CommandsDefault


@pytest.fixture
def commands():
    return CommandsDefault()


def test_char_set(commands):
    assert commands.character_set(CharacterSetVariant.FRANCE).buffer == b'\x1bR\x01'


def test_char_brace(commands):
    assert commands.text("{", encoding='cp437').buffer == b'\x7b'


def test_char_e_accent(commands):
    assert commands.text("é", encoding='cp437').buffer == b'\x82'
