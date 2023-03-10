import sys

from ..printer import DebugPrinter, PrinterNotFound, UsbPrinter
from ..commands import lookup_by_pins
from .test_page import print_test_page
from .poem import print_poem


def usage():
    print('Print a demo page')
    print(f'{sys.argv[0]} demo connector pins [id_vendor] [id_product]')
    print('    demo: test | poem')
    print('    connector: usb')
    print('    pins: 9, 24, 48')
    print('    id_vendor: Vendor identifier (USB)')
    print('    id_product: Product identifier (USB)')
    print('Values id_vendor and id_product should be in hexadecimal. Example for Epson LX-300+II:')
    print(f'{sys.argv[0]} usb 9 0x04b8 0x0005')


def print_function(demo: str):
    match demo:
        case 'test':
            return print_test_page
        case 'poem':
            return print_poem
        case _:
            raise ValueError(f'Unknown demo: {demo}')


def demo(id_vendor: int, id_product: int, pins: int, print_function):
    printer = UsbPrinter(id_vendor=id_vendor, id_product=id_product)
    debug = DebugPrinter()
    commands = lookup_by_pins(pins)
    print_function([debug, printer], commands)


if __name__ == '__main__':
    try:
        demo_scenario = sys.argv[1]
        print_function = print_function(demo_scenario)
        connector = sys.argv[2]
        if connector != 'usb':
            raise ValueError()
        pins = int(sys.argv[3])
        if pins not in [9, 24, 48]:
            raise ValueError()
        id_vendor = int(sys.argv[4], 16)
        id_product = int(sys.argv[5], 16)
    except Exception:
        usage()
        exit(1)

    try:
        demo(id_vendor, id_product, pins, print_function)
    except PrinterNotFound as e:
        print(f'Printer not found: {e}', file=sys.stderr)
        exit(1)
