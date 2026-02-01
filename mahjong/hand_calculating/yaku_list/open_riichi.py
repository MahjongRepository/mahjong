from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class OpenRiichi(Yaku):
    def set_attributes(self) -> None:
        self.yaku_id = 2

        self.name = "Open Riichi"

        self.han_open = None
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
