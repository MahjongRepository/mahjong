from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class YakuhaiOfRound(Yaku):
    yaku_id = 23
    name = "Yakuhai (wind of round)"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
