from collections.abc import Collection, Sequence
from typing import Optional


class Yaku:
    yaku_id: Optional[int]
    tenhou_id: Optional[int]
    name: Optional[str]
    han_open: Optional[int]
    han_closed: Optional[int]
    is_yakuman: Optional[bool]

    def __init__(self, yaku_id: Optional[int] = None) -> None:
        self.tenhou_id = None
        self.yaku_id = yaku_id

        self.set_attributes()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        # for calls in array
        return self.__str__()

    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """
        Is this yaku exists in the hand?
        :param: hand
        :param: args: some yaku requires additional attributes
        :return: boolean
        """
        raise NotImplementedError

    def set_attributes(self) -> None:
        """
        Set id, name, han related to the yaku
        """
        raise NotImplementedError
