import pytest
from src.escp import InvalidEncodingError

from test import CommandsDefault


@pytest.fixture
def commands():
    return CommandsDefault()


@pytest.mark.parametrize('encoding,', ['cp437', 'utf-8'])
def test_encoding_independent(commands, encoding):
    assert commands.text("Hello world", encoding=encoding).buffer == b'Hello world'


usa_char_set_fixture = [
    ('#', b'\x23'), ('$', b'\x24'), ('@', b'\x40'), ('[', b'\x5b'),
    ('\\', b'\x5c'), (']', b'\x5d'), ('^', b'\x5e'), ('`', b'\x60'),
    ('{', b'\x7b'), ('|', b'\x7c'), ('}', b'\x7d'), ('~', b'\x7e')
]


@pytest.mark.parametrize('char,expected', usa_char_set_fixture)
def test_cp437_usa(commands, char, expected):
    assert commands.text(char, encoding='cp437').buffer == expected


@pytest.mark.parametrize('char,expected', usa_char_set_fixture)
def test_utf8_usa(commands, char, expected):
    assert commands.text(char, encoding='utf-8').buffer == expected


def test_utf8_french(commands):
    # should send \x7b with international character set 1 (France)
    with pytest.raises(InvalidEncodingError):
        commands.text("é", encoding='utf-8')


def test_utf8_emoji(commands):
    # Can never be encoded in cp437
    with pytest.raises(InvalidEncodingError):
        commands.text("😢", encoding='utf-8')


def test_cp437_emoji(commands):
    # Can never be encoded in cp437
    with pytest.raises(UnicodeError):
        commands.text("😢", encoding='cp437')
