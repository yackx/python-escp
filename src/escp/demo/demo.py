import sys
import argparse


from ..printer import DebugPrinter, PrinterNotFound, UsbPrinter
from ..commands import lookup_by_pins
from .single_demo import Demo
from .poem import PoemDemo
from .char_tables import CharacterTableDemo
from .i18n_char_set import CharacterSetDemo
from .test_page import TestPage


def make_demo_instance(name: str) -> Demo:
    match name:
        case 'testpage':
            return TestPage()
        case 'poem':
            return PoemDemo()
        case 'chartable':
            return CharacterTableDemo()
        case 'charset':
            return CharacterSetDemo()
        case _:
            raise ValueError(f'Unknown demo: {name}')


def demo(vendor_id: int, product_id: int, pins: int, demo_instance):
    # Actual printer
    printer = UsbPrinter(id_vendor=vendor_id, id_product=product_id, log_io=sys.stdout)
    # Debug (shows the commands with formatting)
    debug = DebugPrinter()
    commands = lookup_by_pins(pins)
    commands = demo_instance.print(commands)
    printer.send(commands.buffer)
    printer.close()
    debug.send(commands.buffer)
    debug.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print a demo page to a USB printer')
    parser.add_argument(
        'demo', type=str, choices=['testpage', 'poem', 'chartable', 'charset'], help='Demo text to send to printer'
    )
    parser.add_argument('-c', '--connector', type=str, required=True, choices=['usb'], help='Connector type')
    parser.add_argument('-p', '--pins', type=int, required=True, choices=[9, 24, 48], help='Number of pins')
    parser.add_argument('--vendor-id', type=str, required=True, help='USB Vendor ID (eg 0x04b8)')
    parser.add_argument('--product-id', type=str, required=True, help='USB Product ID (eg 0x0005)')
    args = parser.parse_args()
    demo_instance = make_demo_instance(args.demo)

    try:
        vendor_id = int(args.vendor_id, 16)
        product_id = int(args.product_id, 16)
    except ValueError:
        print('Invalid vendor/product ID', file=sys.stderr)
        exit(1)

    try:
        demo(vendor_id, product_id, args.pins, demo_instance)
    except PrinterNotFound as e:
        print(f'Printer not found: {e}', file=sys.stderr)
        exit(1)
