from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import classify_hand_suits


class Honitsu(Yaku):
    """
    The hand contains tiles from a single suit plus honours
    """

    yaku_id = 36
    name = "Honitsu"
    han_open = 2
    han_closed = 3

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        suit_mask, honor_count = classify_hand_suits(hand)
        return suit_mask in (1, 2, 4) and honor_count > 0
