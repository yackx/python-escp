import pytest

from src.escp import Commands_9_Pin


@pytest.fixture
def commands():
    return Commands_9_Pin()


@pytest.mark.parametrize('numerator,denominator,codes', [(1, 6, b'\x1b2'), (1, 8, b'\x1b0'), (45, 216, b'\x1b3\x2d')])
def test_line_spacing(commands, numerator, denominator, codes):
    assert commands.line_spacing(numerator, denominator).buffer == codes
