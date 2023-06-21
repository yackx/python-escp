from .single_demo import Demo
from ..commands import CharacterTable, Commands


class CharacterTableDemo(Demo):
    def print(self, cmd: Commands):
        super().print(cmd)
        cmd.init()
        cmd.text('CHARACTER TABLES').cr_lf()
        cmd.text('================').cr_lf(3)
        cmd.text('Samples in this demo: chars [140-149], [160-169]').cr_lf(2)

        for ct in CharacterTable:
            cmd.init().text('# ').text(str(ct)).cr_lf()
            cmd.assign_character_table(1, ct)
            ranges = [range(140, 150), range(160, 170)]
            for rrange in ranges:
                for char in rrange:
                    cmd.text(char)
                cmd.text('  ')
            cmd.cr_lf(2)

        return cmd
