import sys

from .printer import Printer


class OutputPrinter(Printer):

    def __init__(self, output=sys.stdout):
        self.output = output

    def send(self, sequence: bytes):
        self.output.write(str(sequence))
        self.output.flush()

    def close(self):
        close_method = getattr(self.output, 'close', None)
        if callable(close_method):
            close_method()
