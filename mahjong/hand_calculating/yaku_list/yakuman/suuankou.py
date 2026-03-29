from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class Suuankou(Yaku):
    """四暗刻: Four closed pon sets."""

    yaku_id = 102
    name = "Suu Ankou"
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], win_tile: int, is_tsumo: bool) -> bool:
        """
        Check whether the hand contains four closed pon or kan sets.

        :param hand: decomposed hand as a collection of tile groups in 34-format
        :param win_tile: winning tile index in 136-format
        :param is_tsumo: True if the win is by self-draw
        :return: True if the hand contains exactly four closed pon or kan sets
        """
        win_tile //= 4
        closed_hand = []
        for item in hand:
            # if we do the ron on syanpon wait our pon will be consider as open
            if not is_tsumo and win_tile in item and is_pon_or_kan(item):
                continue

            closed_hand.append(item)

        count_of_pon = len([i for i in closed_hand if is_pon_or_kan(i)])
        return count_of_pon == 4
