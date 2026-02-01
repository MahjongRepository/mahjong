from collections.abc import Collection, Sequence

from mahjong.constants import HATSU
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class Hatsu(Yaku):
    """
    Pon of green dragons
    """

    yaku_id = 16
    name = "Yakuhai (hatsu)"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return has_pon_or_kan_of(hand, HATSU)
