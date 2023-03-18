import sys
import argparse


from ..printer import DebugPrinter, PrinterNotFound, UsbPrinter
from ..commands import lookup_by_pins
from .test_page import print_test_page
from .poem import print_poem
from .char_tables import print_char_table
from .i18n_char_set import print_i18n_char_set


def print_function(demo: str):
    match demo:
        case 'testpage':
            return print_test_page
        case 'poem':
            return print_poem
        case 'chartable':
            return print_char_table
        case 'charset':
            return print_i18n_char_set
        case _:
            raise ValueError(f'Unknown demo: {demo}')


def demo(vendor_id: int, product_id: int, pins: int, print_function):
    # Actual printer
    printer = UsbPrinter(id_vendor=vendor_id, id_product=product_id, log_io=sys.stdout)
    # Debug (shows the commands with formatting)
    debug = DebugPrinter()
    commands = lookup_by_pins(pins)
    print_function([printer, debug], commands)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print a demo page')
    parser.add_argument(
        'demo', type=str, choices=['testpage', 'poem', 'chartable', 'charset'], help='Binary file to print'
    )
    parser.add_argument('-c', '--connector', type=str, required=True, choices=['usb'], help='Connector type')
    parser.add_argument('-p', '--pins', type=int, required=True, choices=[9, 24, 48], help='Number of pins')
    parser.add_argument('--vendor-id', type=str, required=True, help='USB Vendor ID (eg 0x04b8)')
    parser.add_argument('--product-id', type=str, required=True, help='USB Product ID (eg 0x0005)')
    args = parser.parse_args()
    print_function = print_function(args.demo)

    try:
        vendor_id = int(args.vendor_id, 16)
        product_id = int(args.product_id, 16)
    except ValueError:
        print('Invalid vendor/product ID', file=sys.stderr)
        exit(1)

    try:
        demo(vendor_id, product_id, args.pins, print_function)
    except PrinterNotFound as e:
        print(f'Printer not found: {e}', file=sys.stderr)
        exit(1)
