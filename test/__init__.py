from src.escp import Commands
from src.escp.commands.commands import T


class CommandsDefault(Commands):
    def line_spacing(self, numerator: int, denominator: int) -> T:
        raise NotImplementedError()

    def is_valid_character_table(self, table: int) -> bool:
        pass
