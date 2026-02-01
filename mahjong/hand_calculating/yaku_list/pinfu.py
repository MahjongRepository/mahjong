from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Pinfu(Yaku):
    """
    Yaku situation
    """

    yaku_id = 12
    name = "Pinfu"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
