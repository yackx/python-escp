import sys

from .printer import Printer


class DebugPrinter(Printer):

    def __init__(self, output=sys.stdout):
        self.output = output

    def send(self, sequence: bytes):
        print_out = lambda x: print(x, file=self.output)
        print_out('-' * 72)
        print_out(str(sequence))
        print_out(str(sequence.hex(':', 1)))

    def close(self):
        pass
