from collections.abc import Collection, Sequence

from mahjong.constants import SOUTH
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class SeatWindSouth(Yaku):
    """
    Seat wind south yakuhai
    """

    yaku_id = 19
    name = "Yakuhai (seat wind south)"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], player_wind: int, round_wind: int, *args) -> bool:
        if player_wind != SOUTH:
            return False
        return has_pon_or_kan_of(hand, SOUTH)
