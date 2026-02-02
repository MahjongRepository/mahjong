from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class UraDora(Yaku):
    yaku_id = 122
    name = "Ura Dora"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True

    def __str__(self) -> str:
        return f"Ura Dora {self.han_closed}"
