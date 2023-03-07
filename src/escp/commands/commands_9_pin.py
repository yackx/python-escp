from typing import Self

from .commands import Commands, int_to_bytes


class Commands_9_Pin(Commands):

    specific_cmds = {
        'line_spacing_n_216': b'\x1b3',
    }

    def _commands(self):
        cmds = super()._commands().copy()
        cmds.update(self.specific_cmds)
        return cmds

    def extra_space(self, value: int) -> Self:
        """Add extra space between characters.

        Add n/120 inch on 9-pin printers.
        """
        return super().extra_space(value)

    def line_spacing(self, numerator: int, denominator: int) -> Self:
        """Set line spacing.

        Changing the line spacing after the page length does not affect the page length.
        Always set the line spacing before the page length.

        Valid combinations: 1/6, 1/8, n/216
        """
        match numerator, denominator:
            case 1, 6:
                return self._append_cmd('line_spacing_1_6')
            case 1, 8:
                return self._append_cmd('line_spacing_1_8')
            case n, 216:
                return self._append_cmd('line_spacing_n_216', int_to_bytes(n))
            case _:
                raise ValueError(f'Invalid line spacing: {numerator}/{denominator}')

