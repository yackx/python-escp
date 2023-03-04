from abc import ABC


class Printer(ABC):

    def send(self, sequence: bytes):
        pass

    def close(self):
        pass
