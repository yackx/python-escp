from ..commands import Commands, Justification, Margin, Typeface
from ..printer import Printer

from .common import print_and_reset


def fox() -> bytes:
    return b'The quick brown fox jumps over the lazy dog'


def lorem() -> bytes:
    return (
        b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor\x0d\x0a'
        b'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\x0d\x0a'
        b'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\x0d\x0a'
        b'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu\x0d\x0a'
        b'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in\x0d\x0a'
        b'culpa qui officia deserunt mollit anim id est laborum.'
    )


def mini_lorem() -> bytes:
    return (
        b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor\x0d\x0a'
        b'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, ...'
    )


def sep_line(count=20) -> bytes:
    return b'-' * count


def print_test_page(printers: [Printer], cmd: Commands):
    def _next_sequence():
        cmd.clear().init().draft(False).typeface(Typeface.SANS_SERIF)

    def _print_and_reset(prepare_next_sequence=True):
        print_and_reset(printers, cmd, _next_sequence if prepare_next_sequence else None)

    # Init
    _print_and_reset()

    # Hello
    cmd.text('ESC/P direct printing test page').cr_lf(2)
    _print_and_reset()

    # Text enhancement
    cmd.text('Text enhancements').cr_lf()
    cmd.text('Bold').cr_lf()
    cmd.bold(True).text(fox()).bold(False).cr_lf()
    cmd.text('Italic').cr_lf()
    cmd.italic(True).text(fox()).italic(False).cr_lf()
    cmd.text('Double strike').cr_lf()
    cmd.double_strike(True).text(fox()).double_strike(False).cr_lf()
    cmd.text('Underline').cr_lf()
    cmd.underline(True).text(fox()).underline(False).cr_lf()
    cmd.cr_lf()
    _print_and_reset()

    # Char width
    cmd.text('Character width').cr_lf()
    for width in [10, 12, 15]:
        cmd \
            .text(f'1/{width} char width') \
            .cr_lf() \
            .character_width(width) \
            .text(fox()) \
            .cr_lf()
    cmd.cr_lf()
    _print_and_reset()

    # Super/subscript
    cmd.text('Superscript').cr_lf()
    cmd.text('Some reference').superscript(True).text('[1]').superscript(False).cr_lf()
    cmd.text('Water is H').subscript(True).text('2').subscript(False).text('O').cr_lf()
    cmd.cr_lf()
    _print_and_reset()

    # Typeface
    cmd.text('Typeface').cr_lf()
    cmd.text('Roman').cr_lf()
    cmd.typeface(Typeface.ROMAN)
    cmd.text('    ').text(fox()).cr_lf()
    cmd.typeface(Typeface.SANS_SERIF)
    cmd.text('Sans Serif').cr_lf()
    cmd.text('    ').text(fox()).cr_lf()
    cmd.cr_lf()
    _print_and_reset()

    # Margins (left)
    cmd.text('Margins (left)')
    for margin in [0, 4, 8]:
        cmd \
            .margin(Margin.LEFT, margin) \
            .text(f'[x] text started at col {margin}') \
            .cr_lf()
    cmd.cr_lf()
    _print_and_reset()

    # Character size
    cmd.text('Character size').cr_lf()
    cmd.double_character_width(True).text('Double character width').double_character_width(False).cr_lf(2)
    cmd.double_character_height(True).text('Double character height').double_character_height(False).cr_lf(2)
    cmd \
        .double_character_width(True) \
        .double_character_height(True) \
        .text('Double character width and height') \
        .double_character_width(False) \
        .double_character_height(False) \
        .cr_lf(2)
    _print_and_reset()

    # Character spacing
    cmd.text('Extra space between characters').cr_lf()
    for extra_space in [1, 5, 10]:
        cmd \
            .text(f'{extra_space}/120"') \
            .cr_lf() \
            .extra_space(extra_space) \
            .text(fox()) \
            .cr_lf()
        _print_and_reset()
    cmd.cr_lf()

    # Condensed
    cmd.text('Condensed text').cr_lf()
    cmd.condensed(True).text(fox()).text('. ').text(fox()).condensed(False).cr_lf(2)
    _print_and_reset()

    # Line spacing
    cmd \
        .text('Line spacing').cr_lf() \
        .text('(not specified)').cr_lf() \
        .text(fox()).cr_lf().text(fox()).cr_lf() \
        .text('1/8').cr_lf() \
        .line_spacing(1, 8) \
        .text(fox()).cr_lf().text(fox()).cr_lf() \
        .text('1/6').cr_lf() \
        .line_spacing(1, 6) \
        .text(fox()).cr_lf().text(fox()).cr_lf() \
        .cr_lf()
    _print_and_reset()

    # Proportional
    cmd.text('Proportional text').cr_lf()
    cmd.proportional(True).text(lorem()).proportional(False).cr_lf(2)
    _print_and_reset()

    # Justification
    cmd.text('Justification (with proportional)').cr_lf()
    cmd.proportional(True)
    cmd.justify(Justification.LEFT).text(fox()).cr_lf()
    cmd.justify(Justification.CENTER).text(fox()).cr_lf()
    cmd.justify(Justification.RIGHT).text(fox()).cr_lf(2)
    _print_and_reset()

    cmd.proportional(True)
    cmd.justify(Justification.CENTER).text(lorem()).cr_lf(2)
    _print_and_reset()

    cmd.proportional(True)
    cmd.justify(Justification.FULL).text(lorem()).cr_lf(2)
    cmd.proportional(False)
    _print_and_reset()

    # Printable control codes
    cmd.text('Printable control codes - upper control codes').cr_lf()
    for i in range(128, 160):
        cmd \
            .text(str(i)) \
            .text(' ') \
            .upper_control_codes_printing(True) \
            .text(i) \
            .upper_control_codes_printing(False) \
            .text('   ')
    cmd.cr_lf()
    _print_and_reset()

    cmd.form_feed()
    _print_and_reset(prepare_next_sequence=False)

    for printer in printers:
        printer.close()
