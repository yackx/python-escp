from typing import TypeVar
from abc import ABC, abstractmethod

from .exceptions import InvalidEncodingError
from .parameters import Margin, PageLengthUnit, Typeface, Justification, CharacterSetVariant, CharacterTable
from .magic_encoding import default_plain_char_substitutions, default_char_set_substitutions


def int_to_bytes(value: int) -> bytes:
    return int.to_bytes(value, length=1, byteorder='big', signed=False)


T = TypeVar('T', bound='Commands')


class Commands(ABC):

    cmds = {
        'init': b'\x1b@',
        'draft': b'\x1bx',
        'cr_lf': b'\x0d\x0a',
        'character_width_10': b'\x1bP',
        'character_width_12': b'\x1bM',
        'character_width_15': b'\x1bg',
        'bold_on': b'\x1bE',
        'bold_off': b'\x1bF',
        'italic_on': b'\x1b4',
        'italic_off': b'\x1b5',
        'double_strike_on': b'\x1bG',
        'double_strike_off': b'\x1bH',
        'underline_on': b'\x1b-\x01',
        'underline_off': b'\x1b-\x00',
        'superscript_on': b'\x1bS\x00',
        'subscript_on': b'\x1bS\x01',
        'superscript_off': b'\x1bT',
        'subscript_off': b'\x1bT',
        'upper_control_codes_printing_on': b'\x1b\x36',
        'upper_control_codes_printing_off': b'\x1b\x37',
        'control_codes_printing': b'\x1b\x49',
        'typeface': b'\x1bk',
        'margin_left': b'\x1bl',
        'margin_right': b'\x1bQ',
        'margin_bottom': b'\x1bN',
        'page_length_in_lines': b'\x1bC',
        'page_length_in_inches': b'\x1bC\x00',
        'double_character_width': b'\x1bW',
        'double_character_width_one_line': b'\x1b\x0e',
        'double_character_height': b'\x1bw',
        'extra_space': b'\x1b ',
        'condensed_on': b'\x1b\x0f',
        'condensed_off': b'\x1b\x12',
        'line_spacing_1_6': b'\x1b2',
        'line_spacing_1_8': b'\x1b0',
        'proportional': b'\x1bp',
        'justify': b'\x1ba',
        'form_feed': b'\x0c',
        'character_set': b'\x1bR',
        'select_character_table': b'\x1b\x74',
        'assign_character_table': b'\x1b\x28\x74',
    }

    _buffer: bytearray

    def __init__(self):
        self.current_character_set = CharacterSetVariant.USA
        self.clear()

    def _commands(self):
        return self.cmds

    def init(self) -> T:
        return self._append_cmd('init')

    def draft(self, enabled: bool) -> T:
        """Change the print quality to draft or letter quality.

        Point sizes 10.5 and 21 only.
        LQ quality for ESC/P2 and ESC/P.
        NLQ for 9-pin printers.
        """
        return self._append_cmd('draft', int_to_bytes(1 if enabled else 0))

    @abstractmethod
    def is_valid_character_table(self, table: int) -> bool:
        """Test if the given character table is valid.

        Depends on the printer number of pins.
        """
        raise NotImplementedError()

    def select_character_table(self, table: int) -> T:
        """Select the character table.

        There are 2 or 4 character tables depending on the printer type [C-77].
        Use the ESC ( t command to assign any registered character table to any character table.

        :param table: Character table number.
        """
        if not self.is_valid_character_table(table):
            raise ValueError(f'Invalid character table {table}')
        return self._append_cmd('select_character_table', int_to_bytes(table))

    def assign_character_table(self, table: int, ct: CharacterTable) -> T:
        """Assign the given character table `ct` to the character `table`.

        :param table: Character table number to assign to.
        :param ct: Character table to assign.
        """
        if not self.is_valid_character_table(table):
            raise ValueError('Invalid character table')
        return self._append_cmd(
            'assign_character_table',
            b'\x03\x00' + int_to_bytes(table) + int_to_bytes(ct.d2) + int_to_bytes(ct.d3)
        )

    def character_set(self, cs: CharacterSetVariant) -> T:
        """Change up to 12 of the characters in the current character table.

        These 12 characters are called international character sets
        because they correspond to characters commonly used in several foreign
        languages. [R-41]

        It is up to the implementer to decide when to set this command
        to the printer to print specific characters.

        :param cs: Character set variant.
        """
        self.current_character_set = cs
        return self._append_cmd('character_set', int_to_bytes(cs.value))

    def text(self, content: bytes | str | int, *, encoding=None) -> T:
        """Add text to the buffer.

        Make sure the string or bytes you send are compatible with the printer encoding.

        This method does not attempt to alter the content to fit the printer capabilities.
        See `magic_text` if you need support for characters that cannot be printed directly.

        This method's exact behavior depends on the content type:
        - If it is a string, it will be byte encoded using the given encoding.
        - If it is an integer, it will be converted to a single byte: 42 -> b'\x2a'.
        - If it is bytes, it will be added as is.

        :param content:
        Text to add. Can be a string, bytes or integer.

        :param encoding:
        Encoding to use when converting a string to bytes.
        The natural encoding for ESC/P is `cp437`, but you can use any compatible encoding.
        Note that the ESC/P2 manual refers to 'PC437' encoding.
        """
        if encoding and not isinstance(encoding, str):
            raise ValueError('encoding valid only for a string')
        if not encoding:
            encoding = 'cp437'

        if isinstance(content, str):
            c = bytes(content, encoding)
            if len(c) != len(content):
                raise InvalidEncodingError(f'length of content encoded to {encoding} mismatches original length')
        elif isinstance(content, int):
            c = int_to_bytes(content)
        elif isinstance(content, bytes):
            c = content
        return self._append(c)

    def magic_text(
            self,
            content: str,
            *,
            character_set_substitution: dict[str, tuple[CharacterSetVariant, bytes]] = None,
            plain_text_substitution: dict[str, bytes] = None,
    ) -> T:
        """Print UTF-8 text using character substitutions and character set switching.

        This method will attempt to issue character set commands in order to print
        the given UTF-8 string.

        It will also perform character substitutions for characters that have
        UTF-8 equivalents in the printer character set.

        For instance, if the string contains an accented character 'é',
        it will switch to French character set (`CharacterSetVariant.FRANCE` i.e. ESC R \x01),
        print the character, and switch back to the original character set.

        The switch occurs only if necessary, i.e. if the character is not available
        in the current character set.

        If an upward arrow '↑' is encountered, it will be replaced by b'\x18'.

        :param content: UTF-8 string to print.
        :param character_set_substitution: Character set substitutions to use.
        :param plain_text_substitution: Plain text substitutions to use.
        """
        if not character_set_substitution:
            character_set_substitution = default_char_set_substitutions
        if not plain_text_substitution:
            plain_text_substitution = default_plain_char_substitutions

        initial_character_set = self.current_character_set
        for c in content:
            try:
                # attempt to use a character substitution, e.g. '↑' becomes b'\x18'
                substitute = plain_text_substitution[c]
                self._append(substitute)
            except KeyError:
                try:
                    # attempt to use a magic character set
                    character_set, code = character_set_substitution[c]
                    if self.current_character_set.value != character_set.value:
                        self.character_set(character_set)
                    self.text(code)
                except KeyError:
                    # treat as a regular character
                    if self.current_character_set.value != initial_character_set.value:
                        self.character_set(initial_character_set)
                    self.text(c)

        if self.current_character_set != initial_character_set:
            self.character_set(initial_character_set)

        return self

    def cr_lf(self, how_many=1) -> T:
        return self._append(self._commands()['cr_lf'] * how_many)

    def bold(self, enabled: bool) -> T:
        return self._append_cmd('bold_on' if enabled else 'bold_off')

    def italic(self, enabled: bool) -> T:
        return self._append_cmd('italic_on' if enabled else 'italic_off')

    def double_strike(self, enabled: bool) -> T:
        """Prints each dot twice, with the second slightly below the first, creating bolder characters.

        On 9-pin printers, NLQ overrides double strike.
        """
        return self._append_cmd('double_strike_on' if enabled else 'double_strike_off')

    def underline(self, enabled: bool) -> T:
        """Turns on/off printing of a line below all characters and spaces"""
        return self._append_cmd('underline_on' if enabled else 'underline_off')

    def character_width(self, width: int) -> T:
        """Select the character width. This may set the point as well.

        :param width: 10, 12 or 15.
        On non- 9-pin printers, the point is set to 10.5 as well.
        """
        if width not in (10, 12, 15):
            raise ValueError(f'Invalid char width: ${width}')
        return self._append_cmd(f'character_width_{width}')

    def superscript(self, enabled: bool) -> T:
        """Prints characters in superscript mode.

        Prints characters that follow at about 2/3 their normal height
        """
        return self._append_cmd('superscript_on' if enabled else 'superscript_off')

    def subscript(self, enabled: bool) -> T:
        """Prints characters in subscript mode.

        Prints characters that follow at about 2/3 their normal height
        """
        return self._append_cmd('subscript_on' if enabled else 'subscript_off')

    def upper_control_codes_printing(self, enabled: bool) -> T:
        """Enable or disable printing of upper control codes.

        If enabled, tells the printer to treat codes from 128 to 159
        as printable characters instead of control code.
        """
        return self._append_cmd('upper_control_codes_printing_on' if enabled else 'upper_control_codes_printing_off')

    def control_codes_printing(self, enabled: bool) -> T:
        """Enable or disable printing of control codes.

        If enabled, tells the printer to treat codes 0–6, 16, 17, 21–23, 25, 26, 28–31, and 128–159 as
        printable character instead of control code.
        """
        return self._append_cmd('control_codes_printing', int_to_bytes(1 if enabled else 0))

    def typeface(self, tf: Typeface) -> T:
        return self._append_cmd('typeface', int_to_bytes(tf.value))

    def margin(self, margin: Margin, value: int) -> T:
        """Set a margin.

        For left and right margins, the value equals the number of characters
        from the left-most mechanically printable position, in the current character pitch.

        The right margin value starts from the left margin.
        Example:
            left margin = 10 (1 inch left margin)
            right margin = 75 (1 inch right margin)

        Top margin is only available on ESC/P2 printers.

        Bottom margin on non ESC/P2 is only available with continuous paper.
        """
        if value < 0 or value > 255:
            raise ValueError(f'Invalid margin value: ${value}')
        if margin == Margin.TOP:
            raise NotImplementedError('Top margin is only available on ESC/P2 printers.')
        return self._append_cmd(f'margin_{margin.name.lower()}', int_to_bytes(value))

    @abstractmethod
    def line_spacing(self, numerator: int, denominator: int) -> T:
        """Set line spacing.

        Changing the line spacing after the page length does not affect the page length.
        Always set the line spacing before the page length.
        """
        raise NotImplementedError()

    def page_length(self, value: int, unit: PageLengthUnit) -> T:
        """Set page length.

        Always set the line spacing before the page length.
        Always set the page length before the paper is loaded
        or when the print position is at the top of the page.
        Setting the page length cancels the bottom margin.

        :param value The number of lines per page
        :param unit The unit of the page length
        """
        cmd = 'page_length_in_inches' if unit == PageLengthUnit.INCHES else 'page_length_in_lines'
        return self._append_cmd(cmd, int_to_bytes(value))

    def double_character_width(self, enabled: bool, one_line=False) -> T:
        """Select double-width printing.

        Doubles the width of all characters, spaces, and intercharacter spacing.
        """
        if one_line and enabled:
            return self._append_cmd('double_character_width_one_line')
        return self._append_cmd('double_character_width', int_to_bytes(1) if enabled else int_to_bytes(0))

    def double_character_height(self, enabled: bool) -> T:
        return self._append_cmd('double_character_height', int_to_bytes(1) if enabled else int_to_bytes(0))

    def extra_space(self, value: int) -> T:
        """Add extra space between characters.

        The fraction of inch depends on the number of pins.
        """
        if value < 0 or value > 255:
            raise ValueError(f'Invalid extra space value: ${value}')
        return self._append_cmd('extra_space', int_to_bytes(value))

    def condensed(self, enabled: bool) -> T:
        """Select condensed printing.

        1/17 inch if 10-cpi selected,
        1/20 inch if 12-cpi selected
        """
        return self._append_cmd('condensed_on' if enabled else 'condensed_off')

    def proportional(self, enabled: bool) -> T:
        """Select proportional printing.

        - Changes made to fixed-pitch printing are not effective until proportional printing is turned off.
        - Condensed printing is not effective when proportional printing is turned on.

        Printers not featuring this command:
        ActionPrinter Apex 80, ActionPrinter T-1000, ActionPrinter 2000, LX-400, LX-800, LX-810,
        LX-850, LX-1050
        """
        return self._append_cmd('proportional', int_to_bytes(1) if enabled else int_to_bytes(0))

    def justify(self, justification: Justification) -> T:
        """Set justification.

        - This is a non-recommended command as per Epson documentation,
          although no explanation is given.
        - Always set justification at the beginning of a line.
        - The printer performs full justification only if the width of the current line is greater than
          75% of the printing area width. If the line width is less than 75%, the printer left-justifies text.
        - You should not use commands that adjust the horizontal print position during full justification.
        - Justification is based on the font selected when the justification command is sent.
          Changing the font after setting justification can cause unpredictable results.
        """
        return self._append_cmd('justify', int_to_bytes(justification.value))

    def form_feed(self) -> T:
        return self._append_cmd('form_feed')

    def _append(self, b: bytes) -> T:
        self._buffer += bytearray(b)
        return self

    def _append_cmd(self, cmd: str, param: bytes = None) -> T:
        seq = self._commands()[cmd]
        if not seq:
            raise RuntimeError(f'No sequence found for {cmd}')
        if param:
            seq += param
        return self._append(seq)

    def clear(self) -> T:
        self._buffer = bytearray()
        return self

    @property
    def buffer(self) -> bytes:
        return bytes(self._buffer)


# Not implemented and reserved to 24/48 pin printers
# Outline + shadow (C-133)
# Scoring (C-127)
# Control paper loading/ejecting (C-157)
