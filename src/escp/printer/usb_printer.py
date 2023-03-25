import typing

import usb.core
import usb.util

from .exceptions import PrinterNotFound
from .printer import Printer


class UsbPrinter(Printer):
    # Reference printer Epson LX-300+II
    # ID_VENDOR = 0x04b8
    # ID_PRODUCT = 0x0005

    device: usb.core.Device | None

    def __init__(
            self,
            *,
            id_vendor: int, id_product: int, endpoint_out=0x01, endpoint_in=0x82, log_io: typing.IO | None = None
    ):
        self.device = None
        self.id_vendor = id_vendor
        self.id_product = id_product
        self.endpoint_out = endpoint_out
        self.endpoint_in = endpoint_in
        self.log_io = log_io

        devices = usb.core.show_devices()
        self.log(devices)

        self.device: usb.core.Device = usb.core.find(idVendor=self.id_vendor, idProduct=self.id_product)
        if not self.device:
            hex_value = lambda x: f'0x{x:04x}'
            raise PrinterNotFound(f'USB id_vendor={hex_value(id_vendor)} id_product={hex_value(id_product)}')
        self.log(str(self.device))
        # TODO Check is printer

        self.detach_kernel_driver()

        self.log("Reset device")
        self.device.reset()

    def detach_kernel_driver(self):
        module: str = self.device.backend.__module__
        self.log(f"Module: ${module}")
        if module.endswith('libusb1'):
            # TODO Explicit check for errno 13 (permission denied)
            check_driver = None
            try:
                check_driver = self.device.is_kernel_driver_active(interface=0)
            except usb.core.USBError as e:
                self.log(f"Failed to check kernel driver activation: ${e}")

            if check_driver is None or check_driver:
                try:
                    self.device.detach_kernel_driver(0)
                except usb.core.USBError as e:
                    self.log(f"Failed to detach kernel driver: ${e}")

    def send(self, sequence: bytes):
        self.device.write(self.endpoint_out, sequence, 5)

    def close(self):
        self.log('Releasing USB')
        if self.device:
            usb.util.dispose_resources(self.device)
        self.device = None
        if self.log_io:
            self.log_io.flush()

    def log(self, message: str):
        if self.log_io:
            self.log_io.write(message)

    def __del__(self):
        self.close()
