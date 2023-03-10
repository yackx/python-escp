from ..commands import Commands, Justification, PageLengthUnit
from ..printer import Printer
from .common import print_and_reset


PAGE_LENGTH_INCHES = 12


def print_poem(printers: [Printer], cmd: Commands):
    def _print_and_reset():
        print_and_reset(printers, cmd)

    text = """When I heard the learn'd astronomer
When the proofs, the figures, were ranged in columns before me
When I was shown the charts and diagrams, to add, divide, and measure them 
When I sitting heard the astronomer where he lectured
with much applause in the lecture-room
How soon unaccountable I became tired and sick
Till rising and gliding out I wander'd off by myself
In the mystical moist night-air, and from time to time
Look'd up in perfect silence at the stars
"""
    cmd \
        .init() \
        .page_length(PAGE_LENGTH_INCHES, PageLengthUnit.INCHES) \
        .justify(Justification.CENTER) \
        .proportional(True) \
        .line_spacing(45, 216) \
        .bold(True).text('When I heard the learn\'d astronomer').bold(False).cr_lf(2) \
        .italic(True).text('by Walt Whitman').italic(False).cr_lf(2) \
        .text(text) \
        .form_feed()
    _print_and_reset()

    for printer in printers:
        printer.close()
