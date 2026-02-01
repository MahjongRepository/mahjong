from collections.abc import Collection, Sequence

from mahjong.constants import SOUTH
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class YakuhaiSouth(Yaku):
    """
    Pon of south winds
    """

    def set_attributes(self) -> None:
        self.yaku_id = 19

        self.name = "Yakuhai (south)"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], player_wind: int, round_wind: int, *args) -> bool:
        if player_wind != SOUTH and round_wind != SOUTH:
            return False
        return has_pon_or_kan_of(hand, SOUTH)
