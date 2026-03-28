from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class RenhouYakuman(Yaku):
    """Non-dealer wins on the first go-around before any calls, scored as yakuman (optional rule)."""

    yaku_id = 117
    name = "Renhou (yakuman)"
    han_closed = 13
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
