from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.constants import CHUN
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class Chun(Yaku):
    """
    Pon of red dragons
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Chun, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 20

        self.name = "Yakuhai (chun)"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return len([x for x in hand if is_pon_or_kan(x) and x[0] == CHUN]) == 1
