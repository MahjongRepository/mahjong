from collections.abc import Collection, Sequence
from typing import Optional

from mahjong.hand_calculating.yaku import Yaku
from mahjong.meld import Meld
from mahjong.utils import is_chi, is_pon_or_kan


class Sanankou(Yaku):
    """
    Three closed pon sets, the other sets need not to be closed
    """

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        super(Sanankou, self).__init__(yaku_id)

    def set_attributes(self) -> None:
        self.tenhou_id = 29

        self.name = "San Ankou"

        self.han_open = 2
        self.han_closed = 2

        self.is_yakuman = False

    def is_condition_met(
        self,
        hand: Collection[Sequence[int]],
        win_tile: int,
        melds: Collection[Meld],
        is_tsumo: bool,
    ) -> bool:
        """
        Three closed pon sets, the other sets need not to be closed
        :param hand: list of hand's sets
        :param win_tile: 136 tiles format
        :param melds: list Meld objects
        :param is_tsumo:
        :return: true|false
        """
        win_tile //= 4

        open_sets = [x.tiles_34 for x in melds if x.opened]

        chi_sets = [x for x in hand if (is_chi(x) and win_tile in x and x not in open_sets)]
        pon_sets = [x for x in hand if is_pon_or_kan(x)]

        closed_pon_sets = []
        for item in pon_sets:
            if item in open_sets:
                continue

            # if we do the ron on syanpon wait our pon will be consider as open
            # and it is not 789999 set
            if win_tile in item and not is_tsumo and not len(chi_sets):
                continue

            closed_pon_sets.append(item)

        return len(closed_pon_sets) == 3
