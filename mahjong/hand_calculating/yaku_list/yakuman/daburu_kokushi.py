from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class DaburuKokushiMusou(Yaku):
    """Kokushi Musou with a thirteen-sided wait (double yakuman)."""

    yaku_id = 112
    name = "Kokushi Musou Juusanmen Matchi"
    han_closed = 26
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
