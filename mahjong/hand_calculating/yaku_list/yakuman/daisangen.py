from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.constants import CHUN, HAKU, HATSU
from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class Daisangen(Yaku):
    """
    The hand contains three sets of dragons
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Daisangen, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 39

        self.name = "Daisangen"

        self.han_open = 13
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        count_of_dragon_pon_sets = 0
        for item in hand:
            if is_pon_or_kan(item) and item[0] in [CHUN, HAKU, HATSU]:
                count_of_dragon_pon_sets += 1
        return count_of_dragon_pon_sets == 3
