from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import classify_hand_suits


class Chinitsu(Yaku):
    """
    The hand contains tiles only from a single suit
    """

    def set_attributes(self) -> None:
        self.yaku_id = 37

        self.name = "Chinitsu"

        self.han_open = 5
        self.han_closed = 6

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        suit_mask, honor_count = classify_hand_suits(hand)
        return honor_count == 0 and suit_mask in (1, 2, 4)
