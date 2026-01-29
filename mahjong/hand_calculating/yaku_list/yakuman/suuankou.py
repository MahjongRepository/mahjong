from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_pon_or_kan


class Suuankou(Yaku):
    """
    Four closed pon sets
    """

    def __init__(self, yaku_id: int | None = None) -> None:
        super(Suuankou, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 41

        self.name = "Suu Ankou"

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], win_tile: int, is_tsumo: bool) -> bool:
        win_tile //= 4
        closed_hand = []
        for item in hand:
            # if we do the ron on syanpon wait our pon will be consider as open
            if is_pon_or_kan(item) and win_tile in item and not is_tsumo:
                continue

            closed_hand.append(item)

        count_of_pon = len([i for i in closed_hand if is_pon_or_kan(i)])
        return count_of_pon == 4
