from abc import ABC

from escp import Commands


class Demo(ABC):
    def print(self, cmd: Commands) -> Commands:
        pass
