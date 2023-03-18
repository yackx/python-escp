import pytest
from escp import CharacterSetVariant

from test import CommandsDefault


@pytest.fixture
def commands():
    return CommandsDefault()


def test_magic_text_no_magic_needed(commands):
    assert commands.magic_text("Hello world").buffer == b'Hello world'


def test_magic_text_no_magic_needed_special_char(commands):
    assert commands.magic_text("Hello $").buffer == b'Hello $'


def test_magic_text_switch_once(commands):
    assert commands.magic_text("Salut à toi").buffer == b'Salut \x1bR\x01\x40\x1bR\x00 toi'


def test_magic_text_switch_once_for_multiple_characters(commands):
    assert commands.magic_text("Salut ààà toi").buffer == b'Salut \x1bR\x01\x40\x40\x40\x1bR\x00 toi'


def test_magic_text_switch_twice(commands):
    assert commands.magic_text("Salut à toi©").buffer == b'Salut \x1bR\x01\x40\x1bR\x00 toi\x1bR\x40\x7b\x1bR\x00'


def test_magic_text_no_switch_already_good_char_set(commands):
    commands.character_set(CharacterSetVariant.FRANCE)
    assert commands.magic_text("Salut à toi").buffer == b'\x1bR\x01Salut \x40 toi'
