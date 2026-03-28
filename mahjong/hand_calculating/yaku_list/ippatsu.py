from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Ippatsu(Yaku):
    """Win within one turn of declaring riichi."""

    yaku_id = 3
    name = "Ippatsu"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
