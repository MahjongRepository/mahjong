from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class KokushiMusou(Yaku):
    """
    国士無双: A hand composed of one of each terminal and honor tile plus one duplicate.

    The duplicate tile determines the winning wait.
    """

    yaku_id = 100
    name = "Kokushi Musou"
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]] | None, tiles_34: Sequence[int], *args) -> bool:
        """
        Check whether the hand is a complete thirteen orphans.

        :param hand: not used for kokushi; pass None
        :param tiles_34: hand in 34-format count array
        :return: True if the hand contains one of each terminal and honor with exactly one duplicate
        """
        return (
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
        )
