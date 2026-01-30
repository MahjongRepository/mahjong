from collections.abc import Collection, Sequence


class Yaku:
    yaku_id: int
    name: str | None
    han_open: int | None
    han_closed: int | None
    is_yakuman: bool | None

    def __init__(self) -> None:
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
