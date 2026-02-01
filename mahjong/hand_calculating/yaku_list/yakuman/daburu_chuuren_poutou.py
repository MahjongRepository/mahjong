from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku


class DaburuChuurenPoutou(Yaku):
    yaku_id = 114
    name = "Daburu Chuuren Poutou"
    han_closed = 26
    is_yakuman = True

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        # was it here or not is controlling by superior code
        return True
