import pytest
from test import CommandsDefault


@pytest.fixture
def commands():
    return CommandsDefault()


@pytest.mark.parametrize(
    'char,expected',
    [('é', b'\x82'), ('è', b'\x8a'), ('ê', b'\x88'), ('ë', b'\x89'), ('æ', b'\x91')]
)
def test_accented_french(commands, char, expected):
    assert commands.text(char).buffer == expected
