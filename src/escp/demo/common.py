from ..commands import Commands
from ..printer import Printer


def print_and_reset(printers: [Printer], cmd: Commands, reset_sequence=None):
    for printer in printers:
        printer.send(cmd.buffer)

    if reset_sequence:
        reset_sequence()
