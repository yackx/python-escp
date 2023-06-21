from .single_demo import Demo
from ..commands import CharacterSetVariant, Commands


class CharacterSetDemo(Demo):

    def print(self, cmd: Commands) -> Commands:
        super().print(cmd)
        cmd.init()

        cmd.text('CHARACTER SET').cr_lf()
        cmd.text('=============').cr_lf(3)

        cmd.text('Sample of the available character sets').cr_lf()
        cmd.text('Sequence: ESC R n').cr_lf()
        cmd.text('ref: R-41').cr_lf(2)

        codes = [35, 36, 64, 91, 92, 93, 94, 96, 123, 124, 125, 126]

        cmd.text(9 * ' ').text('Hex  ')
        for code in codes:
            cmd.text(hex(code)[2:]).text(' ' * 2)
        cmd.cr_lf()

        character_sets = [
            CharacterSetVariant.USA, CharacterSetVariant.FRANCE, CharacterSetVariant.GERMANY, CharacterSetVariant.UK
        ]
        for i18n_char_set in range(0, 4):
            cs = character_sets[i18n_char_set]
            cmd.text('{0:<12}'.format(cs.name))
            cmd.character_set(cs)
            for code in codes:
                cmd.text(chr(code)).text(' ' * 3)
            cmd.cr_lf()

        return cmd
