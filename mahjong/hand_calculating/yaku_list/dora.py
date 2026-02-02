from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Dora(Yaku):
    yaku_id = 120
    name = "Dora"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True

    def __str__(self) -> str:
        return f"Dora {self.han_closed}"
