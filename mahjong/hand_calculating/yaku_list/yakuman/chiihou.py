from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Chiihou(Yaku):
    yaku_id = 116
    name = "Chiihou"
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
