from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.constants import WEST
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class YakuhaiWest(Yaku):
    """
    Pon of west winds
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(YakuhaiWest, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 10

        self.name = "Yakuhai (west)"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], player_wind: int, round_wind: int, *args) -> bool:
        if len([x for x in hand if is_pon_or_kan(x) and x[0] == player_wind]) == 1 and player_wind == WEST:
            return True

        if len([x for x in hand if is_pon_or_kan(x) and x[0] == round_wind]) == 1 and round_wind == WEST:
            return True

        return False
