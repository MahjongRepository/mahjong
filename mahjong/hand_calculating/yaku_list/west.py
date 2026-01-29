from collections.abc import Collection, Sequence

from mahjong.constants import WEST
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class YakuhaiWest(Yaku):
    """
    Pon of west winds
    """

    def __init__(self, yaku_id: int | None = None) -> None:
        super(YakuhaiWest, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 10

        self.name = "Yakuhai (west)"

        self.han_open = 1
        self.han_closed = 1

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], player_wind: int, round_wind: int, *args) -> bool:
        if player_wind != WEST and round_wind != WEST:
            return False
        return has_pon_or_kan_of(hand, WEST)
