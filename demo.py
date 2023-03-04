import sys

import escp


def fox() -> bytes:
    return b'The quick brown fox jumps over the lazy dog'


def lorem() -> bytes:
    return (
        b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor\x0d\x0a'
        b'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\x0d\x0a'
        b'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\x0d\x0a'
        b'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu\x0d\x0a'
        b'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in\x0d\x0a'
        b'culpa qui officia deserunt mollit anim id est laborum.'
    )


def mini_lorem() -> bytes:
    return (
        b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor\x0d\x0a'
        b'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, ...'
    )


def sep_line(count=20) -> bytes:
    return b'-' * count


def print_test_page(printers: [escp.Printer], cmd: escp.Commands):
    def print_and_reset(prepare_next_sequence=True):
        # init printer + clear command buffer
        for printer in printers:
            printer.send(cmd.buffer)

        if prepare_next_sequence:
            cmd.clear().init().draft(False).typeface(escp.Typeface.SANS_SERIF)

    # Init
    print_and_reset()

    # Hello
    cmd.text('ESC/P direct printing test page').cr_lf(2)
    print_and_reset()

    # Text enhancement
    cmd.text('Text enhancements').cr_lf()
    cmd.text('Bold').cr_lf()
    cmd.bold(True).text(fox()).bold(False).cr_lf()
    cmd.text('Italic').cr_lf()
    cmd.italic(True).text(fox()).italic(False).cr_lf()
    cmd.cr_lf()
    print_and_reset()

    # Char width
    cmd.text('Character width').cr_lf()
    for width in [10, 12, 15]:
        cmd \
            .text(f'1/{width} char width') \
            .cr_lf() \
            .character_width(width) \
            .text(fox()) \
            .cr_lf()
    cmd.cr_lf()
    print_and_reset()

    # Typeface
    cmd.text('Typeface').cr_lf()
    cmd.text('Roman').cr_lf()
    cmd.typeface(escp.Typeface.ROMAN)
    cmd.text('    ').text(fox()).cr_lf()
    cmd.typeface(escp.Typeface.SANS_SERIF)
    cmd.text('Sans Serif').cr_lf()
    cmd.text('    ').text(fox()).cr_lf()
    cmd.cr_lf()
    print_and_reset()

    # Margins (left)
    cmd.text('Margins (left)')
    for margin in [0, 4, 8]:
        cmd \
            .margin(escp.Margin.LEFT, margin) \
            .text(f'[x] text started at col {margin}') \
            .cr_lf()
    cmd.cr_lf()
    print_and_reset()

    # Character size
    cmd.text('Character size').cr_lf()
    cmd.double_character_width(True).text('Double character width').double_character_width(False).cr_lf(2)
    cmd.double_character_height(True).text('Double character height').double_character_height(False).cr_lf(2)
    cmd \
        .double_character_width(True) \
        .double_character_height(True) \
        .text('Double character width and height') \
        .double_character_width(False) \
        .double_character_height(False) \
        .cr_lf(2)
    print_and_reset()

    # Character spacing
    cmd.text('Extra space between characters').cr_lf()
    for extra_space in [1, 5, 10]:
        cmd \
            .text(f'{extra_space}/120"') \
            .cr_lf() \
            .extra_space(extra_space) \
            .text(fox()) \
            .cr_lf()
        print_and_reset()
    cmd.cr_lf()

    # Condensed
    cmd.text('Condensed text').cr_lf()
    cmd.condensed(True).text(fox()).text('. ').text(fox()).condensed(False).cr_lf(2)
    print_and_reset()

    # Line spacing
    cmd \
        .text('Line spacing').cr_lf() \
        .text('(not specified)').cr_lf() \
        .text(fox()).cr_lf().text(fox()).cr_lf() \
        .text('1/8').cr_lf() \
        .line_spacing(1, 8) \
        .text(fox()).cr_lf().text(fox()).cr_lf() \
        .text('1/6').cr_lf() \
        .line_spacing(1, 6) \
        .text(fox()).cr_lf().text(fox()).cr_lf() \
        .cr_lf()
    print_and_reset()

    # Proportional
    cmd.text('Proportional text').cr_lf()
    cmd.proportional(True).text(lorem()).proportional(False).cr_lf(2)
    print_and_reset()

    # Justification
    cmd.text('Justification (with proportional)').cr_lf()
    cmd.proportional(True)
    cmd.justify(escp.Justification.LEFT).text(fox()).cr_lf()
    cmd.justify(escp.Justification.CENTER).text(fox()).cr_lf()
    cmd.justify(escp.Justification.RIGHT).text(fox()).cr_lf(2)
    print_and_reset()

    cmd.proportional(True)
    cmd.justify(escp.Justification.CENTER).text(lorem()).cr_lf(2)
    print_and_reset()

    cmd.proportional(True)
    cmd.justify(escp.Justification.FULL).text(lorem()).cr_lf(2)
    cmd.proportional(False)
    print_and_reset(prepare_next_sequence=False)

    for printer in printers:
        printer.close()


def usage():
    print('Print a demo page')
    print(f'{sys.argv[0]} connector pins [id_vendor] [id_product]')
    print('    connector: usb')
    print('    pins: 9, 24, 48')
    print('    id_vendor: Vendor identifier (USB)')
    print('    id_product: Product identifier (USB)')
    print('Values id_vendor and id_product should be in hexadecimal. Example for Epson LX-300+II:')
    print(f'{sys.argv[0]} usb 9 0x04b8 0x0005')


if __name__ == '__main__':
    try:
        connector = sys.argv[1]
        if connector != 'usb':
            raise ValueError()
        pins = int(sys.argv[2])
        if pins not in [9, 24, 48]:
            raise ValueError()
        id_vendor = int(sys.argv[3], 16)
        id_product = int(sys.argv[4], 16)
    except Exception:
        usage()
        exit(1)

    try:
        printer = escp.UsbPrinter(id_vendor=id_vendor, id_product=id_product)
        debug = escp.DebugPrinter()
        commands = escp.lookup_by_pins(pins)
        print_test_page([printer, debug], commands)
    except escp.PrinterNotFound as e:
        print(f'Printer not found: {e}', file=sys.stderr)
        exit(1)
