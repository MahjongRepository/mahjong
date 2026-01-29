from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class YakuhaiOfRound(Yaku):
    def __init__(self, yaku_id: int | None = None) -> None:
        super(YakuhaiOfRound, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 11

        self.name = "Yakuhai (wind of round)"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
