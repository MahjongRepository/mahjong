from collections.abc import Collection, Sequence

from mahjong.constants import SOUTH
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import has_pon_or_kan_of


class RoundWindSouth(Yaku):
    """場風牌 南: Pon of round wind south."""

    yaku_id = 23
    name = "Yakuhai (round wind south)"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], round_wind: int | None, *args) -> bool:
        """
        Check whether the hand contains a pon or kan of the round wind.

        :param hand: decomposed hand as a collection of tile groups in 34-format
        :param round_wind: tile index in 34-format of the round wind
        :return: True if the round wind matches and the hand has a pon or kan of it
        """
        if round_wind != SOUTH:
            return False
        return has_pon_or_kan_of(hand, SOUTH)
