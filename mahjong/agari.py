# -*- coding: utf-8 -*-
import copy

from mahjong.utils import find_isolated_tile_indices


class Agari(object):

    def is_agari(self, tiles_34, open_sets_34=None):
        """
        Determine was it win or not
        :param tiles_34: 34 tiles format array
        :param open_sets_34: array of array of 34 tiles format
        :return: boolean
        """
        # we will modify them later, so we need to use a copy
        tiles = copy.deepcopy(tiles_34)

        # With open hand we need to remove open sets from hand and replace them with isolated pon sets
        # it will allow to determine agari state correctly
        if open_sets_34:
            isolated_tiles = find_isolated_tile_indices(tiles)
            for meld in open_sets_34:
                if not isolated_tiles:
                    break

                isolated_tile = isolated_tiles.pop()

                tiles[meld[0]] -= 1
                tiles[meld[1]] -= 1
                tiles[meld[2]] -= 1
                tiles[isolated_tile] = 3

        j = (1 << tiles[27]) | (1 << tiles[28]) | (1 << tiles[29]) | (1 << tiles[30]) | \
            (1 << tiles[31]) | (1 << tiles[32]) | (1 << tiles[33])

        if j >= 0x10:
            return False

        # 13 orphans
        if ((j & 3) == 2) and (tiles[0] * tiles[8] * tiles[9] * tiles[17] * tiles[18] *
                               tiles[26] * tiles[27] * tiles[28] * tiles[29] * tiles[30] *
                               tiles[31] * tiles[32] * tiles[33] == 2):
            return True

        # seven pairs
        if not (j & 10) and sum([tiles[i] == 2 for i in range(0, 34)]) == 7:
            return True

        if j & 2:
            return False

        n00 = tiles[0] + tiles[3] + tiles[6]
        n01 = tiles[1] + tiles[4] + tiles[7]
        n02 = tiles[2] + tiles[5] + tiles[8]

        n10 = tiles[9] + tiles[12] + tiles[15]
        n11 = tiles[10] + tiles[13] + tiles[16]
        n12 = tiles[11] + tiles[14] + tiles[17]

        n20 = tiles[18] + tiles[21] + tiles[24]
        n21 = tiles[19] + tiles[22] + tiles[25]
        n22 = tiles[20] + tiles[23] + tiles[26]

        n0 = (n00 + n01 + n02) % 3
        if n0 == 1:
            return False

        n1 = (n10 + n11 + n12) % 3
        if n1 == 1:
            return False

        n2 = (n20 + n21 + n22) % 3
        if n2 == 1:
            return False

        if ((n0 == 2) + (n1 == 2) + (n2 == 2) + (tiles[27] == 2) + (tiles[28] == 2) +
                (tiles[29] == 2) + (tiles[30] == 2) + (tiles[31] == 2) + (tiles[32] == 2) +
                (tiles[33] == 2) != 1):
            return False

        nn0 = (n00 * 1 + n01 * 2) % 3
        m0 = self._to_meld(tiles, 0)
        nn1 = (n10 * 1 + n11 * 2) % 3
        m1 = self._to_meld(tiles, 9)
        nn2 = (n20 * 1 + n21 * 2) % 3
        m2 = self._to_meld(tiles, 18)

        if j & 4:
            return not (n0 | nn0 | n1 | nn1 | n2 | nn2) and self._is_mentsu(m0) \
                and self._is_mentsu(m1) and self._is_mentsu(m2)

        if n0 == 2:
            return not (n1 | nn1 | n2 | nn2) and self._is_mentsu(m1) and self._is_mentsu(m2) \
                and self._is_atama_mentsu(nn0, m0)

        if n1 == 2:
            return not (n2 | nn2 | n0 | nn0) and self._is_mentsu(m2) and self._is_mentsu(m0) \
                and self._is_atama_mentsu(nn1, m1)

        if n2 == 2:
            return not (n0 | nn0 | n1 | nn1) and self._is_mentsu(m0) and self._is_mentsu(m1) \
                and self._is_atama_mentsu(nn2, m2)

        return False

    def _is_mentsu(self, m):
        a = m & 7
        b = 0
        c = 0
        if a == 1 or a == 4:
            b = c = 1
        elif a == 2:
            b = c = 2
        m >>= 3
        a = (m & 7) - b

        if a < 0:
            return False

        is_not_mentsu = False
        for x in range(0, 6):
            b = c
            c = 0
            if a == 1 or a == 4:
                b += 1
                c += 1
            elif a == 2:
                b += 2
                c += 2
            m >>= 3
            a = (m & 7) - b
            if a < 0:
                is_not_mentsu = True
                break

        if is_not_mentsu:
            return False

        m >>= 3
        a = (m & 7) - c

        return a == 0 or a == 3

    def _is_atama_mentsu(self, nn, m):
        if nn == 0:
            if (m & (7 << 6)) >= (2 << 6) and self._is_mentsu(m - (2 << 6)):
                return True
            if (m & (7 << 15)) >= (2 << 15) and self._is_mentsu(m - (2 << 15)):
                return True
            if (m & (7 << 24)) >= (2 << 24) and self._is_mentsu(m - (2 << 24)):
                return True
        elif nn == 1:
            if (m & (7 << 3)) >= (2 << 3) and self._is_mentsu(m - (2 << 3)):
                return True
            if (m & (7 << 12)) >= (2 << 12) and self._is_mentsu(m - (2 << 12)):
                return True
            if (m & (7 << 21)) >= (2 << 21) and self._is_mentsu(m - (2 << 21)):
                return True
        elif nn == 2:
            if (m & (7 << 0)) >= (2 << 0) and self._is_mentsu(m - (2 << 0)):
                return True
            if (m & (7 << 9)) >= (2 << 9) and self._is_mentsu(m - (2 << 9)):
                return True
            if (m & (7 << 18)) >= (2 << 18) and self._is_mentsu(m - (2 << 18)):
                return True
        return False

    def _to_meld(self, tiles, d):
        result = 0
        for i in range(0, 9):
            result |= (tiles[d + i] << i * 3)
        return result
