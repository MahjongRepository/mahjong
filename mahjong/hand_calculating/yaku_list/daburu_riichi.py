from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class DaburuRiichi(Yaku):
    """Riichi declared on the player's first turn."""

    yaku_id = 8
    name = "Double Riichi"
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
