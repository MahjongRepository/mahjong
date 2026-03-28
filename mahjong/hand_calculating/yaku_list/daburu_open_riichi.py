from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class DaburuOpenRiichi(Yaku):
    """Open riichi declared on the player's first turn (optional rule)."""

    yaku_id = 9
    name = "Double Open Riichi"
    han_closed = 3

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
