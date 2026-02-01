from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class YakuhaiOfPlace(Yaku):
    def set_attributes(self) -> None:
        self.yaku_id = 22

        self.name = "Yakuhai (wind of place)"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
