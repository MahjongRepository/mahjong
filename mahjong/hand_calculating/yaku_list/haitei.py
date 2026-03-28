from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class Haitei(Yaku):
    """Win by self-draw on the last tile from the wall."""

    yaku_id = 6
    name = "Haitei Raoyue"
    han_open = 1
    han_closed = 1

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """Return True unconditionally; this yaku is awarded by the hand evaluation logic."""
        return True
