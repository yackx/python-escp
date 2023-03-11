from ..commands import Commands, Justification, PageLengthUnit, CharacterTable
from ..printer import Printer
from .common import print_and_reset


PAGE_LENGTH_INCHES = 12


def print_char_table(printers: [Printer], cmd: Commands):
    def _print_and_reset():
        print_and_reset(printers, cmd)

    cmd.init().cr_lf(4)
    for i in (0, 1):
        cmd \
            .init() \
            .text('Character table - SELECT ').text(i).cr_lf() \
            .select_character_table(i) \
            .text('0123456789 ABCDEF #$@[\]^`{|}~').cr_lf()
        cmd.cr_lf(3)
    _print_and_reset()

    cmd.text('Character table - SET').cr_lf()

    for ct in CharacterTable:
        cmd.init().text('# ').text(str(ct)).cr_lf()
        cmd.assign_character_table(1, ct)
        for c in range(140, 150):
            cmd.text(c)
        cmd.text(' ')
        for c in range(160, 170):
            cmd.text(c)
        cmd.cr_lf()
    _print_and_reset()

    for printer in printers:
        printer.close()
