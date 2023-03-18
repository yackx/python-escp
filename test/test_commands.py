import pytest
from src.escp import Margin, PageLengthUnit, Typeface

from test import CommandsDefault


@pytest.fixture
def commands():
    return CommandsDefault()


def test_draft_mode_on(commands):
    assert commands.draft(True).buffer == b'\x1bx\x01'


def test_draft_mode_off(commands):
    assert commands.draft(False).buffer == b'\x1bx\x00'


def test_text_str(commands):
    assert commands.text("Hello world").buffer == b'Hello world'


def test_text_bytes(commands):
    assert commands.text(b"Hello world").buffer == b'Hello world'


def test_text_int(commands):
    assert commands.text(42).buffer == b'*'


def test_cr_lf(commands):
    assert commands.cr_lf().buffer == b'\x0d\x0a'


def test_cr_lf_several(commands):
    assert commands.cr_lf(2).buffer == b'\x0d\x0a\x0d\x0a'


def test_bold_on(commands):
    assert commands.bold(True).buffer == b'\x1bE'


def test_bold_off(commands):
    assert commands.bold(False).buffer == b'\x1bF'


def test_double_strike_on(commands):
    assert commands.double_strike(True).buffer == b'\x1bG'


def test_double_strike_off(commands):
    assert commands.double_strike(False).buffer == b'\x1bH'


def test_italic_on(commands):
    assert commands.italic(True).buffer == b'\x1b4'


def test_italic_off(commands):
    assert commands.italic(False).buffer == b'\x1b5'


def test_underline_on(commands):
    assert commands.underline(True).buffer == b'\x1b-\x01'


def test_underline_off(commands):
    assert commands.underline(False).buffer == b'\x1b-\x00'


@pytest.mark.parametrize("width,byte_param", [(10, b'\x1bP'), (12, b'\x1bM'), (15, b'\x1bg')])
def test_character_width(commands, width, byte_param):
    assert commands.character_width(width).buffer == byte_param


def test_character_width_invalid(commands):
    with pytest.raises(ValueError):
        commands.character_width(11)


def test_superscript_on(commands):
    assert commands.superscript(True).buffer == b'\x1bS\x00'


def test_superscript_off(commands):
    assert commands.superscript(False).buffer == b'\x1bT'


def test_subscript_on(commands):
    assert commands.subscript(True).buffer == b'\x1bS\x01'


def test_subscript_off(commands):
    assert commands.subscript(False).buffer == b'\x1bT'


def test_upper_control_codes_printing_on(commands):
    assert commands.upper_control_codes_printing(True).buffer == b'\x1b\x36'


def test_upper_control_codes_printing_off(commands):
    assert commands.upper_control_codes_printing(False).buffer == b'\x1b\x37'


def test_control_codes_printing_on(commands):
    assert commands.control_codes_printing(True).buffer == b'\x1b\x49\x01'


def test_control_codes_printing_off(commands):
    assert commands.control_codes_printing(False).buffer == b'\x1b\x49\x00'


@pytest.mark.parametrize('typeface,value', [(Typeface.ROMAN, b'\x1bk\x00'), (Typeface.SANS_SERIF, b'\x1bk\x01')])
def test_typeface(commands, typeface, value):
    assert commands.typeface(typeface).buffer == value


@pytest.mark.parametrize(
    'side,codes', [
        (Margin.RIGHT, b'\x1bQ\x05'),
        (Margin.BOTTOM, b'\x1bN\x05'),
        (Margin.LEFT, b'\x1bl\x05'),
    ]
)
def test_margin(commands, side, codes):
    assert commands.margin(side, 5).buffer == codes


def test_margin_invalid(commands):
    with pytest.raises(NotImplementedError):
        commands.margin(Margin.TOP, 5)


def test_line_spacing(commands):
    with pytest.raises(NotImplementedError):
        commands.line_spacing(1, 1)


def test_page_length_in_lines(commands):
    assert commands.page_length(20, PageLengthUnit.LINES).buffer == b'\x1b\x43\x14'


def test_page_length_in_lines(commands):
    assert commands.page_length(20, PageLengthUnit.LINES).buffer == b'\x1b\x43\x14'


def test_page_length_in_inch(commands):
    assert commands.page_length(20, PageLengthUnit.INCHES).buffer == b'\x1bC\x00\x14'


def test_clear(commands):
    commands.text("Hello world")
    assert commands.clear().buffer == b''
