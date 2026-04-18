from collections.abc import Sequence
from itertools import chain

from mahjong.constants import TERMINAL_AND_HONOR_INDICES


class Shanten:
    """
    Shanten (minimum tiles to tenpai/agari) calculation.

    The shanten number represents how many tiles away a hand is from being complete (agari).
    A shanten number of 0 means the hand is tenpai (one tile away from winning),
    and -1 means the hand is already complete.

    Accepts tile counts that correspond to valid game states: 1, 2, 4, 5, 7, 8, 10, 11, 13, or 14.
    Tile counts divisible by 3 (0, 3, 6, 9, 12) are rejected because they never occur
    in real riichi mahjong gameplay (a hand is always 3n+1 or 3n+2 tiles).

    Supports three hand types: regular (4 melds + 1 pair), chiitoitsu (seven pairs),
    and kokushi musou (thirteen orphans).
    """

    TENPAI_STATE = 0
    """Hand is tenpai — one tile away from winning."""

    AGARI_STATE = -1
    """Hand is complete (agari)."""

    @staticmethod
    def calculate_shanten(tiles_34: Sequence[int], use_chiitoitsu: bool = True, use_kokushi: bool = True) -> int:
        """
        Return the minimum shanten number across regular, chiitoitsu, and kokushi hand types.

        A pair alone is a complete hand (remaining melds are implied open):

        >>> tiles_34 = [0] * 34
        >>> tiles_34[0] = 2
        >>> Shanten.calculate_shanten(tiles_34)
        -1

        A triplet with an isolated tile is tenpai (one tile needed for the pair):

        >>> tiles_34 = [0] * 34
        >>> tiles_34[0] = 3
        >>> tiles_34[9] = 1
        >>> Shanten.calculate_shanten(tiles_34)
        0

        :param tiles_34: hand in 34-format count array (length 34)
        :param use_chiitoitsu: include seven pairs pattern in calculation
        :param use_kokushi: include thirteen orphans pattern in calculation
        :return: minimum shanten number (-1 for agari, 0 for tenpai, positive for tiles needed)
        :raises ValueError: if tile count exceeds 14 or is divisible by 3
        """
        count_of_tiles = sum(tiles_34)
        shanten_results = [_RegularShanten(tiles_34).calculate(count_of_tiles)]

        if count_of_tiles >= 13:
            if use_chiitoitsu:
                shanten_results.append(Shanten.calculate_shanten_for_chiitoitsu_hand(tiles_34))
            if use_kokushi:
                shanten_results.append(Shanten.calculate_shanten_for_kokushi_hand(tiles_34))

        return min(shanten_results)

    @staticmethod
    def calculate_shanten_for_chiitoitsu_hand(tiles_34: Sequence[int]) -> int:
        """
        Calculate the shanten number for a chiitoitsu (seven pairs) hand.

        Count the number of pairs and unique tile kinds to determine
        how far the hand is from completing seven distinct pairs.

        Seven distinct pairs form a complete hand:

        >>> tiles_34 = [2, 2, 2, 2, 2, 2, 2] + [0] * 27
        >>> Shanten.calculate_shanten_for_chiitoitsu_hand(tiles_34)
        -1

        Six pairs with two singles — tenpai:

        >>> tiles_34 = [2, 2, 2, 2, 2, 2, 1, 1] + [0] * 26
        >>> Shanten.calculate_shanten_for_chiitoitsu_hand(tiles_34)
        0

        :param tiles_34: hand in 34-format count array (length 34)
        :return: shanten number for chiitoitsu (-1 for complete, 0-6 otherwise)
        """
        pairs = len([x for x in tiles_34 if x >= 2])
        if pairs == 7:
            return Shanten.AGARI_STATE

        kinds = len([x for x in tiles_34 if x >= 1])
        return 6 - pairs + (7 - kinds if kinds < 7 else 0)

    @staticmethod
    def calculate_shanten_for_kokushi_hand(tiles_34: Sequence[int]) -> int:
        """
        Calculate the shanten number for a kokushi musou (thirteen orphans) hand.

        Kokushi requires one of each terminal (1, 9 of each suit) and each honor tile,
        plus one duplicate. Count how many of the 13 required tiles are present
        and whether any appears twice.

        All 13 terminal/honor tiles with one duplicate form a complete hand:

        >>> tiles_34 = [0] * 34
        >>> for i in [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]:
        ...    tiles_34[i] = 1
        >>> tiles_34[33] = 2
        >>> Shanten.calculate_shanten_for_kokushi_hand(tiles_34)
        -1

        :param tiles_34: hand in 34-format count array (length 34)
        :return: shanten number for kokushi (-1 for complete, 0-13 otherwise)
        """
        completed_terminals = 0
        terminals = 0
        for i in TERMINAL_AND_HONOR_INDICES:
            completed_terminals += tiles_34[i] >= 2
            terminals += tiles_34[i] != 0

        return 13 - terminals - (1 if completed_terminals else 0)

    @staticmethod
    def calculate_shanten_for_regular_hand(tiles_34: Sequence[int]) -> int:
        """
        Calculate the shanten number for a regular hand (4 melds + 1 pair).

        The number of melds to be calculated is determined based on the number of tiles in the hand.
        The number of melds is determined as ``number_of_tiles // 3``
        (e.g., 0 for 1-2 tiles, 1 for 4-5 tiles, ..., 4 for 13-14 tiles).
        If there are fewer than 4 melds, the remaining melds are treated as open melds.

        Use a depth-first search over all possible meld/pair/tatsu decompositions
        of the suited tiles (indices 0-26), after pre-processing honor tiles (indices 27-33).

        A pair alone is a complete hand (remaining melds are implied open):

        >>> tiles_34 = [0] * 34
        >>> tiles_34[0] = 2
        >>> Shanten.calculate_shanten_for_regular_hand(tiles_34)
        -1

        A triplet with an isolated tile is tenpai:

        >>> tiles_34 = [0] * 34
        >>> tiles_34[0] = 3
        >>> tiles_34[9] = 1
        >>> Shanten.calculate_shanten_for_regular_hand(tiles_34)
        0

        :param tiles_34: hand in 34-format count array (length 34)
        :return: shanten number for regular hand (-1 for complete, 0+ otherwise)
        :raises ValueError: if tile count exceeds 14 or is divisible by 3
        """
        count_of_tiles = sum(tiles_34)
        return _RegularShanten(tiles_34).calculate(count_of_tiles)

    @staticmethod
    def calculate_shanten_for_regular_hand_3p(tiles_34: Sequence[int]) -> int:
        count_of_tiles = sum(tiles_34)
        return _RegularShanten(tiles_34).calculate_3p(count_of_tiles)


class _RegularShanten:
    def __init__(self, tiles_34: Sequence[int]) -> None:
        # we will modify tiles array later, so we need to use a copy
        self._tiles = list(tiles_34)
        self._number_melds = 0
        self._number_tatsu = 0
        self._number_pairs = 0
        self._number_jidahai = 0
        self._flag_four_copies = 0
        self._flag_isolated_tiles = 0
        self._min_shanten = 8

    def calculate(self, count_of_tiles: int) -> int:
        if count_of_tiles > 14:
            msg = f"Too many tiles = {count_of_tiles}"
            raise ValueError(msg)

        if count_of_tiles % 3 == 0:
            msg = f"Invalid tile count = {count_of_tiles}. Valid counts: 1, 2, 4, 5, 7, 8, 10, 11, 13, 14."
            raise ValueError(msg)

        self._remove_character_tiles(count_of_tiles)

        init_mentsu = (14 - count_of_tiles) // 3
        self._scan(init_mentsu)

        return self._min_shanten

    def calculate_3p(self, count_of_tiles: int) -> int:
        if any(self._tiles[1:8]):
            msg = "Invalid tile for three player"
            raise ValueError(msg)

        if count_of_tiles > 14:
            msg = f"Too many tiles = {count_of_tiles}"
            raise ValueError(msg)

        if count_of_tiles % 3 == 0:
            msg = f"Invalid tile count = {count_of_tiles}. Valid counts: 1, 2, 4, 5, 7, 8, 10, 11, 13, 14."
            raise ValueError(msg)

        self._remove_character_tiles_3p(count_of_tiles)

        init_mentsu = (14 - count_of_tiles) // 3
        self._scan_3p(init_mentsu)

        return self._min_shanten

    def _scan(self, init_mentsu: int) -> None:
        for i in range(27):
            self._flag_four_copies |= (self._tiles[i] == 4) << i
        self._number_melds += init_mentsu
        self._run(0)

    def _scan_3p(self, init_mentsu: int) -> None:
        for i in range(27):
            self._flag_four_copies |= (self._tiles[i] == 4) << i
        self._number_melds += init_mentsu
        self._run(9)

    def _run(self, depth: int) -> None:
        if self._min_shanten == Shanten.AGARI_STATE:
            return None

        while not self._tiles[depth]:
            depth += 1

            if depth >= 27:
                break

        if depth >= 27:
            return self._update_result()

        i = depth
        if i > 8:
            i -= 9
        if i > 8:
            i -= 9

        if self._tiles[depth] == 4:
            self._increase_set(depth)
            if i < 7 and self._tiles[depth + 2]:
                if self._tiles[depth + 1]:
                    self._increase_syuntsu(depth)
                    self._run(depth + 1)
                    self._decrease_syuntsu(depth)
                self._increase_tatsu_second(depth)
                self._run(depth + 1)
                self._decrease_tatsu_second(depth)

            if i < 8 and self._tiles[depth + 1]:
                self._increase_tatsu_first(depth)
                self._run(depth + 1)
                self._decrease_tatsu_first(depth)

            self._increase_isolated_tile(depth)
            self._run(depth + 1)
            self._decrease_isolated_tile(depth)
            self._decrease_set(depth)
            self._increase_pair(depth)

            if i < 7 and self._tiles[depth + 2]:
                if self._tiles[depth + 1]:
                    self._increase_syuntsu(depth)
                    self._run(depth)
                    self._decrease_syuntsu(depth)
                self._increase_tatsu_second(depth)
                self._run(depth + 1)
                self._decrease_tatsu_second(depth)

            if i < 8 and self._tiles[depth + 1]:
                self._increase_tatsu_first(depth)
                self._run(depth + 1)
                self._decrease_tatsu_first(depth)

            self._decrease_pair(depth)

        if self._tiles[depth] == 3:
            self._increase_set(depth)
            self._run(depth + 1)
            self._decrease_set(depth)
            self._increase_pair(depth)

            if i < 7 and self._tiles[depth + 1] and self._tiles[depth + 2]:
                self._increase_syuntsu(depth)
                self._run(depth + 1)
                self._decrease_syuntsu(depth)
            else:
                if i < 7 and self._tiles[depth + 2]:
                    self._increase_tatsu_second(depth)
                    self._run(depth + 1)
                    self._decrease_tatsu_second(depth)

                if i < 8 and self._tiles[depth + 1]:
                    self._increase_tatsu_first(depth)
                    self._run(depth + 1)
                    self._decrease_tatsu_first(depth)

            self._decrease_pair(depth)

            if i < 7 and self._tiles[depth + 2] >= 2 and self._tiles[depth + 1] >= 2:
                self._increase_syuntsu(depth)
                self._increase_syuntsu(depth)
                self._run(depth)
                self._decrease_syuntsu(depth)
                self._decrease_syuntsu(depth)

        if self._tiles[depth] == 2:
            self._increase_pair(depth)
            self._run(depth + 1)
            self._decrease_pair(depth)
            if i < 7 and self._tiles[depth + 2] and self._tiles[depth + 1]:
                self._increase_syuntsu(depth)
                self._run(depth)
                self._decrease_syuntsu(depth)

        if self._tiles[depth] == 1:
            if i < 6 and self._tiles[depth + 1] == 1 and self._tiles[depth + 2] and self._tiles[depth + 3] != 4:
                self._increase_syuntsu(depth)
                self._run(depth + 2)
                self._decrease_syuntsu(depth)
            else:
                self._increase_isolated_tile(depth)
                self._run(depth + 1)
                self._decrease_isolated_tile(depth)

                if i < 7 and self._tiles[depth + 2]:
                    if self._tiles[depth + 1]:
                        self._increase_syuntsu(depth)
                        self._run(depth + 1)
                        self._decrease_syuntsu(depth)
                    self._increase_tatsu_second(depth)
                    self._run(depth + 1)
                    self._decrease_tatsu_second(depth)

                if i < 8 and self._tiles[depth + 1]:
                    self._increase_tatsu_first(depth)
                    self._run(depth + 1)
                    self._decrease_tatsu_first(depth)

        return None

    def _update_result(self) -> None:
        ret_shanten = 8 - self._number_melds * 2 - self._number_tatsu - self._number_pairs
        n_mentsu_kouho = self._number_melds + self._number_tatsu
        if self._number_pairs:
            n_mentsu_kouho += self._number_pairs - 1
        elif (
            self._flag_four_copies
            and self._flag_isolated_tiles
            and (self._flag_four_copies | self._flag_isolated_tiles) == self._flag_four_copies
        ):
            ret_shanten += 1

        if n_mentsu_kouho > 4:
            ret_shanten += n_mentsu_kouho - 4

        if ret_shanten != Shanten.AGARI_STATE and ret_shanten < self._number_jidahai:
            ret_shanten = self._number_jidahai

        self._min_shanten = min(self._min_shanten, ret_shanten)

    def _increase_set(self, k: int) -> None:
        self._tiles[k] -= 3
        self._number_melds += 1

    def _decrease_set(self, k: int) -> None:
        self._tiles[k] += 3
        self._number_melds -= 1

    def _increase_pair(self, k: int) -> None:
        self._tiles[k] -= 2
        self._number_pairs += 1

    def _decrease_pair(self, k: int) -> None:
        self._tiles[k] += 2
        self._number_pairs -= 1

    def _increase_syuntsu(self, k: int) -> None:
        self._tiles[k] -= 1
        self._tiles[k + 1] -= 1
        self._tiles[k + 2] -= 1
        self._number_melds += 1

    def _decrease_syuntsu(self, k: int) -> None:
        self._tiles[k] += 1
        self._tiles[k + 1] += 1
        self._tiles[k + 2] += 1
        self._number_melds -= 1

    def _increase_tatsu_first(self, k: int) -> None:
        self._tiles[k] -= 1
        self._tiles[k + 1] -= 1
        self._number_tatsu += 1

    def _decrease_tatsu_first(self, k: int) -> None:
        self._tiles[k] += 1
        self._tiles[k + 1] += 1
        self._number_tatsu -= 1

    def _increase_tatsu_second(self, k: int) -> None:
        self._tiles[k] -= 1
        self._tiles[k + 2] -= 1
        self._number_tatsu += 1

    def _decrease_tatsu_second(self, k: int) -> None:
        self._tiles[k] += 1
        self._tiles[k + 2] += 1
        self._number_tatsu -= 1

    def _increase_isolated_tile(self, k: int) -> None:
        self._tiles[k] -= 1
        self._flag_isolated_tiles |= 1 << k

    def _decrease_isolated_tile(self, k: int) -> None:
        self._tiles[k] += 1
        self._flag_isolated_tiles &= ~(1 << k)

    def _remove_character_tiles(self, nc: int) -> None:
        four_copies = 0
        isolated = 0

        for i in range(27, 34):
            if self._tiles[i] == 4:
                self._number_melds += 1
                self._number_jidahai += 1
                four_copies |= 1 << (i - 27)
                isolated |= 1 << (i - 27)

            if self._tiles[i] == 3:
                self._number_melds += 1

            if self._tiles[i] == 2:
                self._number_pairs += 1

            if self._tiles[i] == 1:
                isolated |= 1 << (i - 27)

        if self._number_jidahai and (nc % 3) == 2:
            self._number_jidahai -= 1

        if isolated:
            self._flag_isolated_tiles |= 1 << 27
            if (four_copies | isolated) == four_copies:
                self._flag_four_copies |= 1 << 27

    def _remove_character_tiles_3p(self, nc: int) -> None:
        four_copies = 0
        isolated = 0

        for flag_pos, i in enumerate(chain(range(27, 34), [0, 8])):
            if self._tiles[i] == 4:
                self._number_melds += 1
                self._number_jidahai += 1
                four_copies |= 1 << flag_pos
                isolated |= 1 << flag_pos

            if self._tiles[i] == 3:
                self._number_melds += 1

            if self._tiles[i] == 2:
                self._number_pairs += 1

            if self._tiles[i] == 1:
                isolated |= 1 << flag_pos

        if self._number_jidahai and (nc % 3) == 2:
            self._number_jidahai -= 1

        if isolated:
            self._flag_isolated_tiles |= 1 << 27
            if (four_copies | isolated) == four_copies:
                self._flag_four_copies |= 1 << 27
