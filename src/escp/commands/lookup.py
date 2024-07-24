from .commands import Commands
from .commands_9_pin import Commands_9_Pin
from .commands_24_48_pin import Commands_24_48_Pin


def lookup_by_pins(pins) -> Commands:
    """Lookup commands by the number of pins."""
    match pins:
        case 9:
            return Commands_9_Pin()
        case 24 | 48:
            return Commands_24_48_Pin()
        case _:
            raise ValueError(f'Invalid number of pins: {pins}')
