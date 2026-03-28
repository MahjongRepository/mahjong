from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class DaburuChuurenPoutou(Yaku):
    """Chuuren Poutou with a nine-sided wait (double yakuman)."""

    yaku_id = 114
    name = "Daburu Chuuren Poutou"
    han_closed = 26
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
