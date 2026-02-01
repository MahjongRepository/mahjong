from abc import ABC, abstractmethod
from collections.abc import Collection, Sequence


class Yaku(ABC):
    yaku_id: int
    name: str
    # 0 means the yaku is not available in the respective hand type
    han_open: int = 0
    han_closed: int = 0
    is_yakuman: bool = False

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        # for calls in array
        return self.__str__()

    @abstractmethod
    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """
        Is this yaku exists in the hand?
        :param: hand
        :param: args: some yaku requires additional attributes
        :return: boolean
        """
