from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.hand_calculating.yaku import Yaku


class OpenRiichi(Yaku):
    def __init__(self, yaku_id: Optional[int]) -> None:
        super(OpenRiichi, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.name = "Open Riichi"

        self.han_open = None
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
