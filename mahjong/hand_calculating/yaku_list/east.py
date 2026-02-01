from collections.abc import Collection, Sequence

from mahjong.constants import EAST
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class YakuhaiEast(Yaku):
    """
    Pon of east winds
    """

    def set_attributes(self) -> None:
        self.yaku_id = 18

        self.name = "Yakuhai (east)"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], player_wind: int, round_wind: int, *args) -> bool:
        if player_wind != EAST and round_wind != EAST:
            return False
        return has_pon_or_kan_of(hand, EAST)
