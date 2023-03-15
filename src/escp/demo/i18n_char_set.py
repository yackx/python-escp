from escp import CharacterSetVariant

from ..commands import Commands, Justification, PageLengthUnit, CharacterTable
from ..printer import Printer
from .common import print_and_reset


PAGE_LENGTH_INCHES = 12


def print_i18n_char_set(printers: [Printer], cmd: Commands):
    def _print_and_reset():
        print_and_reset(printers, cmd)

    cmd.init()

    cmd.text('CHARACTER SET').cr_lf()
    cmd.text('=============').cr_lf(3)

    cmd.text('Sample of the available character sets').cr_lf()
    cmd.text('Sequence: ESC R n').cr_lf()
    cmd.text('ref: R-41').cr_lf(2)

    codes = [35, 36, 64, 91, 92, 93, 94, 96, 123, 124, 125, 126]

    cmd.text(9 * ' ').text('Hex  ')
    for code in codes:
        cmd.text(hex(code)[2:]).text(' ' * 2)
    cmd.cr_lf()

    character_sets = [
        CharacterSetVariant.USA, CharacterSetVariant.FRANCE, CharacterSetVariant.GERMANY, CharacterSetVariant.UK
    ]
    for i18n_char_set in range(0, 4):
        cs = character_sets[i18n_char_set]
        cmd.text('{0:<12}'.format(cs.name))
        cmd.character_set(cs)
        for code in codes:
            cmd.text(chr(code)).text(' ' * 3)
        cmd.cr_lf()
    cmd.form_feed()

    _print_and_reset()

    for printer in printers:
        printer.close()
