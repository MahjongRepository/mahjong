"""
Abstract base for yaku pattern detection.

Defines the :class:`Yaku` base class that every concrete yaku inherits.
Each subclass represents one scoring pattern (e.g., tanyao, riichi, kokushi musou)
and implements :meth:`~Yaku.is_condition_met` to test whether the pattern is
present in a given hand decomposition.

Concrete yaku are located in the :mod:`~mahjong.hand_calculating.yaku_list`
and :mod:`~mahjong.hand_calculating.yaku_list.yakuman` packages.
"""

from abc import ABC, abstractmethod
from collections.abc import Collection, Sequence


class Yaku(ABC):
    """
    Abstract base class for all yaku.

    Subclasses must set the class attributes below and implement
    :meth:`is_condition_met`.  A han value of ``0`` means the yaku is
    unavailable for that hand type (open or closed).

    >>> from mahjong.hand_calculating.yaku_list import Iipeiko
    >>> iipeiko = Iipeiko()
    >>> iipeiko.yaku_id
    14
    >>> iipeiko.han_open
    0
    >>> iipeiko.han_closed
    1
    >>> iipeiko.is_yakuman
    False
    >>> str(iipeiko)
    'Iipeiko'

    :ivar yaku_id: unique numeric identifier for this yaku
    :vartype yaku_id: int
    :ivar name: display name of the yaku (e.g., ``"Tanyao"``, ``"Kokushi Musou"``)
    :vartype name: str
    :ivar han_open: han awarded when the hand is open; ``0`` if not available for open hands
    :vartype han_open: int
    :ivar han_closed: han awarded when the hand is closed; ``0`` if not available for closed hands
    :vartype han_closed: int
    :ivar is_yakuman: ``True`` for yakuman-level patterns (13+ han)
    :vartype is_yakuman: bool
    """

    yaku_id: int
    """Unique numeric identifier for this yaku."""
    name: str
    """Display name of the yaku (e.g., ``"Tanyao"``, ``"Kokushi Musou"``)."""
    han_open: int = 0
    """Han awarded for open hands.  ``0`` means the yaku is not available when the hand is open."""
    han_closed: int = 0
    """Han awarded for closed hands.  ``0`` means the yaku is not available when the hand is closed."""
    is_yakuman: bool = False
    """Whether this yaku is a yakuman (worth 13 han or more)."""

    def __str__(self) -> str:
        """Return the yaku name."""
        return self.name

    def __repr__(self) -> str:
        """Return the yaku name (used when printing lists of yaku)."""
        return self.__str__()

    @abstractmethod
    def is_condition_met(self, hand: Collection[Sequence[int]], *args) -> bool:
        """
        Determine whether this yaku is present in the given hand decomposition.

        The base signature accepts only the decomposed hand, but concrete subclasses may
        require additional positional arguments depending on the yaku.  Common extra
        parameters include:

        * ``player_wind`` / ``round_wind`` — for yakuhai wind checks
        * ``win_tile``, ``melds``, ``is_tsumo`` — for yaku that depend on win conditions
          (e.g., san ankou, suu ankou)
        * ``tiles_34`` — for kokushi, which uses the raw count array instead of a
          decomposed hand

        :param hand: decomposed hand as a collection of tile groups in 34-format
        :param args: additional attributes required by the specific yaku subclass
        :return: ``True`` if the yaku condition is satisfied
        """
