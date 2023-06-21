from .single_demo import Demo
from ..commands import Commands, Justification


class PoemDemo(Demo):

    def print(self, cmd: Commands) -> Commands:
        super().print(cmd)

        text = """When I heard the learn'd astronomer
When the proofs, the figures, were ranged in columns before me
When I was shown the charts and diagrams, to add, divide, and measure them 
When I sitting heard the astronomer where he lectured
with much applause in the lecture-room
How soon unaccountable I became tired and sick
Till rising and gliding out I wander'd off by myself
In the mystical moist night-air, and from time to time
Look'd up in perfect silence at the stars
"""
        return cmd \
            .init() \
            .justify(Justification.CENTER) \
            .proportional(True) \
            .line_spacing(45, 216) \
            .bold(True).text('When I heard the learn\'d astronomer').bold(False).cr_lf(2) \
            .italic(True).text('by Walt Whitman').italic(False).cr_lf(2) \
            .text(text) \
            .cr_lf(4)
