from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class NagashiMangan(Yaku):
    """All discards are terminals and honors with no calls against them."""

    yaku_id = 10
    name = "Nagashi Mangan"
    han_open = 5
    han_closed = 5

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
