# escp

**A Python library to drive ESC/P printers**

## Motivation

There is **no driver** available for your printer, or there is one but it is **slow** and the **print quality is mediocre**.

Missing driver can be worked around by using a generic 9-pin or 24-pin generic driver. To get the highest quality, this library focuses on **text mode** printing, leveraging device fonts (built-in fonts), as opposed to modern drivers that rely on graphics.

![Printing sample on a 9-pin Epson LX-300+II](escp.jpg)

## Installation

```bash
pip install escp
```

## Use

Only USB is supported for now. You can find the `id_vendor` and `id_product` values using `lsusb`.

```bash
$ lsusb | grep -i epson
Bus 001 Device 004: ID 04b8:0005 Seiko Epson Corp. Printer
```

```python
import escp

# Create a printer instance (Espon LX-300+II)
printer = escp.UsbPrinter(id_vendor=0x04b8, id_product=0x0005)
# Obtain commands for 9-pin printer
commands = escp.lookup_by_pins(9)
# Prepare the buffer to print a short text
commands.init().text('ESC/P direct printing test page').cr_lf(2)
# Printer go brrrrrr
printer.send(commands.buffer)
```

See  [demo](src/escp/demo.py) for a more complete example.

## Features

### ESC/P, ESC/P2, ESC/POS

| Variant | Supported |
|---------|-----------|
| ESC/P   | ✓         |
| ESC/P2  | ✗         |
| ESC/POS | ✗         |

- **ESC/P** (Epson Standard Code for Printers), sometimes called *Escape/P*, is a printer control language developed by Epson to control computer printers. It was mainly used in dot matrix printers and some inkjet printers, and is still widely used in many receipt thermal printers. Supported. Primary target.
- **ESC/P2** is a more recent variant of ESC/P by Epson. Backward compatible with ESC/P. Not supported. Switch to ESC/P but some features won't be available.
- **ESC/POS** is a variant for controlling receipt printers as commonly used at the point of sale (POS). Often thermal printers. Not supported and out of scope. Use the comprehensive [python-escpos](https://github.com/python-escpos/python-escpos) library instead.

References

- [Epson reference manual (dec. 1997)](https://files.support.epson.com/pdf/general/escp2ref.pdf)
- [Wikipedia](https://en.wikipedia.org/wiki/ESC/P)

### Printers

Tested on a 9-pin reference printer: **Epson LX-300+II**. All 9-pin printers should work, with minor hardware limitations on some commands. 24/48-pin printers are implemented bt not tested. The differences between 9-pin and 24/48 pin are minor.

| Type       | Status                                    |
|------------|-------------------------------------------|
| 9-pin      | Work in progress – Text mode              |
| 24/48-pin  | Work in progress – Text mode – Not tested |

### Connectivity

| Connector | Status |
|-----------|------- |
| USB       | ✓      |
| Serial    | ✗      |
| Parallel  | ✗      |
| File      | ✓      |

Although serial and parallel ports are not supported, you can output the printer commands to a file and send it in raw mode to the printer using `lpr`.

## Credits

Inspired from [python-escpos](https://github.com/python-escpos/python-escpos).

## License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.txt)
