from collections.abc import Collection, Sequence

from mahjong.constants import HAKU
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class Haku(Yaku):
    """
    Pon of white dragons
    """

    def __init__(self, yaku_id: int | None = None) -> None:
        super(Haku, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 18

        self.name = "Yakuhai (haku)"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return has_pon_or_kan_of(hand, HAKU)
