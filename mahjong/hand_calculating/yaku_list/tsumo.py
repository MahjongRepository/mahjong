from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Tsumo(Yaku):
    """Win by self-draw with a closed hand."""

    yaku_id = 0
    name = "Menzen Tsumo"
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
