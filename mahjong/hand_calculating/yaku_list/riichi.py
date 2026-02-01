from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Riichi(Yaku):
    yaku_id = 1
    name = "Riichi"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
