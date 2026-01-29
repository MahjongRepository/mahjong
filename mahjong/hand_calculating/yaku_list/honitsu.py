from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import classify_hand_suits


class Honitsu(Yaku):
    """
    The hand contains tiles from a single suit plus honours
    """

    def __init__(self, yaku_id: int | None = None) -> None:
        super(Honitsu, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 34
        self.name = "Honitsu"

        self.han_open = 2
        self.han_closed = 3

        self.is_yakuman = False

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        suit_mask, honor_count = classify_hand_suits(hand)
        return suit_mask in (1, 2, 4) and honor_count > 0
