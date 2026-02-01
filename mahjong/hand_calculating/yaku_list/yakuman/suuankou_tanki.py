from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class SuuankouTanki(Yaku):
    yaku_id = 113
    name = "Suu Ankou Tanki"
    han_closed = 26
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        return True
