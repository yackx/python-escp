from typing import Self

from .parameters import PageLengthUnit
from .commands import Commands


class Commands_24_48_Pin(Commands):

    specific_cmds = {
        'line_spacing_n_180': b'\x1b3',
        'line_spacing_n_360': b'\x1b+',
    }

    def __init__(self, *, debug=False):
        super().__init__()

    def _commands(self):
        return super()._commands().update(self.specific_cmds)

    def page_length(self, value: int, unit: PageLengthUnit) -> Self:
        """Set page length.

        The value is the number of lines per page.
        """
        pass

    def extra_space(self, value: int) -> Self:
        """Add extra space between characters.

        Add n/180 inch on 24/48-pin printers in LQ mode,
        n/120 inch on 24/48-pin printers in Draft mode.
        """
        return super().extra_space(value)

    def line_spacing(self, numerator: int, denominator: int) -> 'Commands':
        """Set line spacing.

        Changing the line spacing after the page length does not affect the page length.
        Always set the line spacing before the page length.

        Valid combinations: 1/6, 1/8, n/180, n/360
        """
        match numerator, denominator:
            case 1, 6:
                return self._append_cmd('line_spacing_1_6')
            case 1, 8:
                return self._append_cmd('line_spacing_1_8')
            case n, 180:
                return self._append_cmd('line_spacing_n_180', bytes(n))
            case n, 360:
                return self._append_cmd('line_spacing_n_360', bytes(n))
            case _:
                raise ValueError(f'Invalid line spacing: {numerator}/{denominator}')
