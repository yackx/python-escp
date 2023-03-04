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
    def print_and_clear_buffer():
        for printer in printers:
            printer.send(cmd.buffer)
        cmd.clear()

    cmd.text(fox()).cr_lf(2)
    print_and_clear_buffer()

    for width in [10, 12, 15]:
        cmd \
            .text(f'1/{width} char width') \
            .cr_lf() \
            .character_width(width) \
            .text(fox()) \
            .cr_lf()
    print_and_clear_buffer()

    cmd.bold(True).text('Bold text').bold(False).cr_lf()
    cmd.italic(True).text('Italic text').italic(False).cr_lf()
    print_and_clear_buffer()

    cmd.typeface(escp.Typeface.ROMAN).text('Roman typeface').cr_lf().text(fox()).cr_lf()
    cmd.typeface(escp.Typeface.SANS_SERIF).text('Sans-serif typeface').cr_lf().text(fox()).cr_lf()
    print_and_clear_buffer()

    for margin in [0, 4, 8]:
        cmd \
            .margin(escp.Margin.LEFT, margin) \
            .text(f'Left margin {margin}') \
            .cr_lf()
    print_and_clear_buffer()

    cmd.double_character_width(True).text('Double character width').double_character_width(False).cr_lf()
    cmd.double_character_height(True).text('Double character height').double_character_height(False).cr_lf()
    cmd \
        .double_character_width(True) \
        .double_character_height(True) \
        .text('Double character width and height') \
        .double_character_width(False) \
        .double_character_height(False)
    print_and_clear_buffer()

    cmd.text('Extra space between characters').cr_lf()
    for extra_space in [10, 60, 120]:
        cmd \
            .extra_space(extra_space) \
            .text(fox()) \
            .text(f'    ({extra_space}/120")') \
            .cr_lf()
    print_and_clear_buffer()

    cmd.condensed(True).text('Condensed text').condensed(False).cr_lf()
    print_and_clear_buffer()

    cmd \
        .text('Line spacing') \
        .cr_lf() \
        .text('Line spacing (not specified)') \
        .cr_lf() \
        .line_spacing(1, 8) \
        .text('Line spacing 1/8"') \
        .cr_lf() \
        .line_spacing(1, 6) \
        .text('Line spacing 1/6"') \
        .cr_lf() \
        .line_spacing(1, 8)
    print_and_clear_buffer()

    for printer in printers:
        printer.close()


def usage():
    print('Print a demo page')
    print(f'    {sys.argv[0]} id_vendor id_product')
    print('Values should be in hexadecimal. Example for Epson LX-300+II:')
    print(f'    {sys.argv[0]} 0x04b8 0x0005')


if __name__ == '__main__':
    try:
        id_vendor = int(sys.argv[1], 16)
        id_product = int(sys.argv[2], 16)
    except Exception:
        usage()
        exit(1)

    printer = escp.UsbPrinter(id_vendor=id_vendor, id_product=id_product)
    debug = escp.DebugPrinter()
    commands = escp.Commands_9_Pin()
    print_test_page([printer, debug], commands)
