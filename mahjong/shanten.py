from collections.abc import Sequence

from mahjong.constants import TERMINAL_AND_HONOR_INDICES


class Shanten:
    TENPAI_STATE = 0
    AGARI_STATE = -1

    @staticmethod
    def calculate_shanten(tiles_34: Sequence[int], use_chiitoitsu: bool = True, use_kokushi: bool = True) -> int:
        """
        Return the minimum shanten for provided hand,
        it will consider chiitoitsu and kokushi options if possible.
        """

        shanten_results = [Shanten.calculate_shanten_for_regular_hand(tiles_34)]
        if use_chiitoitsu:
            shanten_results.append(Shanten.calculate_shanten_for_chiitoitsu_hand(tiles_34))
        if use_kokushi:
            shanten_results.append(Shanten.calculate_shanten_for_kokushi_hand(tiles_34))

        return min(shanten_results)

    @staticmethod
    def calculate_shanten_for_chiitoitsu_hand(tiles_34: Sequence[int]) -> int:
        """
        Calculate the number of shanten for chiitoitsu hand
        """
        pairs = len([x for x in tiles_34 if x >= 2])
        if pairs == 7:
            return Shanten.AGARI_STATE

        kinds = len([x for x in tiles_34 if x >= 1])
        return 6 - pairs + (7 - kinds if kinds < 7 else 0)

    @staticmethod
    def calculate_shanten_for_kokushi_hand(tiles_34: Sequence[int]) -> int:
        """
        Calculate the number of shanten for kokushi musou hand
        """
        completed_terminals = 0
        terminals = 0
        for i in TERMINAL_AND_HONOR_INDICES:
            completed_terminals += tiles_34[i] >= 2
            terminals += tiles_34[i] != 0

        return 13 - terminals - (completed_terminals and 1 or 0)

    @staticmethod
    def calculate_shanten_for_regular_hand(tiles_34: Sequence[int]) -> int:
        """
        Calculate the number of shanten for regular hand
        """
        return _RegularShanten(tiles_34).calculate()


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

    def calculate(self) -> int:
        count_of_tiles = sum(self._tiles)
        assert count_of_tiles <= 14, f"Too many tiles = {count_of_tiles}"

        self._remove_character_tiles(count_of_tiles)

        init_mentsu = (14 - count_of_tiles) // 3
        self._scan(init_mentsu)

        return self._min_shanten

    def _scan(self, init_mentsu: int) -> None:
        for i in range(0, 27):
            self._flag_four_copies |= (self._tiles[i] == 4) << i
        self._number_melds += init_mentsu
        self._run(0)

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

    def _update_result(self) -> None:
        ret_shanten = 8 - self._number_melds * 2 - self._number_tatsu - self._number_pairs
        n_mentsu_kouho = self._number_melds + self._number_tatsu
        if self._number_pairs:
            n_mentsu_kouho += self._number_pairs - 1
        elif self._flag_four_copies and self._flag_isolated_tiles:
            if (self._flag_four_copies | self._flag_isolated_tiles) == self._flag_four_copies:
                ret_shanten += 1

        if n_mentsu_kouho > 4:
            ret_shanten += n_mentsu_kouho - 4

        if ret_shanten != Shanten.AGARI_STATE and ret_shanten < self._number_jidahai:
            ret_shanten = self._number_jidahai

        if ret_shanten < self._min_shanten:
            self._min_shanten = ret_shanten

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
