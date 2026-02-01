from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class KokushiMusou(Yaku):
    """
    A hand composed of one of each of the terminals and honour tiles plus
    any tile that matches anything else in the hand.
    """

    yaku_id = 100
    name = "Kokushi Musou"
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]] | None, tiles_34: Sequence[int], *args) -> bool:
        if (
            tiles_34[0]
            * tiles_34[8]
            * tiles_34[9]
            * tiles_34[17]
            * tiles_34[18]
            * tiles_34[26]
            * tiles_34[27]
            * tiles_34[28]
            * tiles_34[29]
            * tiles_34[30]
            * tiles_34[31]
            * tiles_34[32]
            * tiles_34[33]
            == 2
        ):
            return True
