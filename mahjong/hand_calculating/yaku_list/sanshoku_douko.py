from collections.abc import Collection, Sequence

from mahjong.hand_calculating.yaku import Yaku
from mahjong.utils import is_man, is_pin, is_pon_or_kan, is_sou, simplify


class SanshokuDoukou(Yaku):
    """
    Three pon sets consisting of the same numbers in all three suits
    """

    yaku_id = 31
    name = "Sanshoku Doukou"
    han_open = 2
    han_closed = 2

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        pon_sets = [i for i in hand if is_pon_or_kan(i)]
        if len(pon_sets) < 3:
            return False

        sou_pon: list[Collection[int]] = []
        pin_pon: list[Collection[int]] = []
        man_pon: list[Collection[int]] = []
        for item in pon_sets:
            if is_sou(item[0]):
                sou_pon.append(item)
            elif is_pin(item[0]):
                pin_pon.append(item)
            elif is_man(item[0]):
                man_pon.append(item)

        for sou_item in sou_pon:
            for pin_item in pin_pon:
                for man_item in man_pon:
                    # cast tile indices to 1..9 representation
                    sou_item = {simplify(x) for x in sou_item}
                    pin_item = {simplify(x) for x in pin_item}
                    man_item = {simplify(x) for x in man_item}
                    if sou_item == pin_item == man_item:
                        return True
        return False
