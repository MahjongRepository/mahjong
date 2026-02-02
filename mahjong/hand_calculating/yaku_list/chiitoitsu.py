from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Chiitoitsu(Yaku):
    """
    Hand contains only pairs
    """

    yaku_id = 34
    name = "Chiitoitsu"
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return len(hand) == 7
