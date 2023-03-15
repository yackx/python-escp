from ..commands import Commands, Justification, PageLengthUnit, CharacterTable
from ..printer import Printer
from .common import print_and_reset


PAGE_LENGTH_INCHES = 12


def print_char_table(printers: [Printer], cmd: Commands):
    def _print_and_reset():
        print_and_reset(printers, cmd)

    cmd.init()

    cmd.text('CHARACTER TABLES').cr_lf()
    cmd.text('================').cr_lf(3)
    cmd.text('Samples: 140-149, 160-169').cr_lf(2)

    for ct in CharacterTable:
        cmd.init().text('# ').text(str(ct)).cr_lf()
        cmd.assign_character_table(1, ct)
        ranges = [range(140, 150), range(160, 170)]
        for rrange in ranges:
            for char in rrange:
                cmd.text(char)
            cmd.text('  ')
        cmd.cr_lf(2)
    cmd.form_feed()

    _print_and_reset()

    for printer in printers:
        printer.close()
