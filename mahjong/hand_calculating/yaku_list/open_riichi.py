from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class OpenRiichi(Yaku):
    yaku_id = 2
    name = "Open Riichi"
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
