from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class SuuankouTanki(Yaku):
    def __init__(self, yaku_id: int | None = None) -> None:
        super(SuuankouTanki, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 40

        self.name = "Suu Ankou Tanki"

        self.han_open = None
        self.han_closed = 26

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
