from collections.abc import Collection, Sequence

from mahjong.constants import HAKU
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class Haku(Yaku):
    """
    Pon of white dragons
    """

    yaku_id = 15
    name = "Yakuhai (haku)"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return has_pon_or_kan_of(hand, HAKU)
