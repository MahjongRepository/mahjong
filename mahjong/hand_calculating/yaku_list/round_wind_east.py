from collections.abc import Collection, Sequence

from mahjong.constants import EAST
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class RoundWindEast(Yaku):
    """
    Round wind east yakuhai
    """

    yaku_id = 22
    name = "Yakuhai (round wind east)"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], player_wind: int, round_wind: int, *args) -> bool:
        if round_wind != EAST:
            return False
        return has_pon_or_kan_of(hand, EAST)
