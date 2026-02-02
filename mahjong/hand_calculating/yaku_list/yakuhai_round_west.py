from collections.abc import Collection, Sequence

from mahjong.constants import WEST
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class RoundWest(Yaku):
    """
    Round wind west yakuhai
    """

    yaku_id = 24
    name = "Yakuhai (round wind west)"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], player_wind: int, round_wind: int, *args) -> bool:
        if round_wind != WEST:
            return False
        return has_pon_or_kan_of(hand, WEST)
