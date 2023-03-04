import sys

import usb.core
import usb.util

from .printer import Printer
from .exceptions import PrinterNotFound


class UsbPrinter(Printer):
    # Reference printer Epson LX-300+II
    # ID_VENDOR = 0x04b8
    # ID_PRODUCT = 0x0005

    device: usb.core.Device | None

    def __init__(self, *, id_vendor, id_product, endpoint_out=0x01, endpoint_in=0x82):
        self.device = None
        self.id_vendor = id_vendor
        self.id_product = id_product
        self.endpoint_out = endpoint_out
        self.endpoint_in = endpoint_in

        devices = usb.core.show_devices()
        print(devices)

        self.device: usb.core.Device = usb.core.find(idVendor=self.id_vendor, idProduct=self.id_product)
        if not self.device:
            hex = lambda x: f'0x{x:04x}'
            raise PrinterNotFound(f'USB id_vendor={hex(id_vendor)} id_product={hex(id_product)}')
        print(self.device)
        # TODO Check is printer

        self.detach_kernel_driver()

        print("Reset device")
        self.device.reset()

    def detach_kernel_driver(self):
        module: str = self.device.backend.__module__
        print(f"Module: ${module}")
        if module.endswith('libusb1'):
            # TODO Explicit check for errno 13 (permission denied)
            check_driver = None
            try:
                check_driver = self.device.is_kernel_driver_active(interface=0)
            except usb.core.USBError as e:
                print(f"Failed to check kernel driver activation: ${e}", file=sys.stderr)

            if check_driver is None or check_driver:
                try:
                    self.device.detach_kernel_driver(0)
                except usb.core.USBError as e:
                    print(f"Failed to detach kernel driver: ${e}", file=sys.stderr)

    def send(self, sequence: bytes):
        self.device.write(self.endpoint_out, sequence, 5)

    def close(self):
        print('Releasing USB')
        if self.device:
            usb.util.dispose_resources(self.device)
        self.device = None
