from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.meld import Meld
from mahjong.utils import is_chi, is_pon_or_kan


class Sanankou(Yaku):
    """
    Three closed pon sets, the other sets need not to be closed
    """

    yaku_id = 31
    name = "San Ankou"
    han_open = 2
    han_closed = 2

    def is_condition_met(
        self,
        hand: Collection[Sequence[int]],
        win_tile: int,
        melds: Collection[Meld],
        is_tsumo: bool,
    ) -> bool:
        win_tile_34 = win_tile // 4

        open_sets: set[tuple[int, ...]] = set()
        for m in melds:
            if m.opened:
                open_sets.add(tuple(m.tiles_34))

        has_chi_with_win_tile = False
        closed_pon_count = 0

        for item in hand:
            item_tuple = tuple(item)

            if is_pon_or_kan(item):
                if item_tuple not in open_sets:
                    closed_pon_count += 1
            elif is_chi(item) and win_tile_34 in item and item_tuple not in open_sets:
                has_chi_with_win_tile = True

        # if ron on syanpon wait and no closed chi with win tile, that pon is considered open
        if not is_tsumo and not has_chi_with_win_tile:
            for item in hand:
                if is_pon_or_kan(item) and item[0] == win_tile_34 and tuple(item) not in open_sets:
                    closed_pon_count -= 1
                    break

        return closed_pon_count == 3
