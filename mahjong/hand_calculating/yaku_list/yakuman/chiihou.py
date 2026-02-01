from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Chiihou(Yaku):
    def set_attributes(self) -> None:
        self.yaku_id = 116

        self.name = "Chiihou"

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
