from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.hand_calculating.yaku import Yaku


class Tsumo(Yaku):
    """
    Yaku situation
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Tsumo, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 0
        self.name = "Menzen Tsumo"

        self.han_open = None
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
