from collections.abc import Collection, Sequence

from mahjong.constants import WEST
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class YakuhaiWest(Yaku):
    """
    Pon of west winds
    """

    yaku_id = 20
    name = "Yakuhai (west)"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], player_wind: int, round_wind: int, *args) -> bool:
        if WEST not in (player_wind, round_wind):
            return False
        return has_pon_or_kan_of(hand, WEST)
