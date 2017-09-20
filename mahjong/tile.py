# -*- coding: utf-8 -*-


class Tile(object):
    value = None
    is_tsumogiri = None

    def __init__(self, value, is_tsumogiri):
        self.value = value
        self.is_tsumogiri = is_tsumogiri


class TilesConverter(object):

    @staticmethod
    def to_one_line_string(tiles):
        """
        Convert 136 tiles array to the one line string
        Example of output 123s123p123m33z
        """
        tiles = sorted(tiles)

        man = [t for t in tiles if t < 36]

        pin = [t for t in tiles if 36 <= t < 72]
        pin = [t - 36 for t in pin]

        sou = [t for t in tiles if 72 <= t < 108]
        sou = [t - 72 for t in sou]

        honors = [t for t in tiles if t >= 108]
        honors = [t - 108 for t in honors]

        sou = sou and ''.join([str((i // 4) + 1) for i in sou]) + 's' or ''
        pin = pin and ''.join([str((i // 4) + 1) for i in pin]) + 'p' or ''
        man = man and ''.join([str((i // 4) + 1) for i in man]) + 'm' or ''
        honors = honors and ''.join([str((i // 4) + 1) for i in honors]) + 'z' or ''

        return man + pin + sou + honors

    @staticmethod
    def to_34_array(tiles):
        """
        Convert 136 array to the 34 tiles array
        """
        results = [0] * 34
        for tile in tiles:
            tile //= 4
            results[tile] += 1
        return results

    @staticmethod
    def to_136_array(tiles):
        """
        Convert 34 array to the 136 tiles array
        """
        temp = []
        results = []
        for x in range(0, 34):
            if tiles[x]:
                temp_value = [x * 4] * tiles[x]
                for tile in temp_value:
                    if tile in results:
                        count_of_tiles = len([x for x in temp if x == tile])
                        new_tile = tile + count_of_tiles
                        results.append(new_tile)

                        temp.append(tile)
                    else:
                        results.append(tile)
                        temp.append(tile)
        return results

    @staticmethod
    def string_to_136_array(sou=None, pin=None, man=None, honors=None):
        """
        Method to convert one line string tiles format to the 136 array
        We need it to increase readability of our tests
        """
        def _split_string(string, offset):
            data = []
            temp = []

            if not string:
                return []

            for i in string:
                tile = offset + (int(i) - 1) * 4
                if tile in data:
                    count_of_tiles = len([x for x in temp if x == tile])
                    new_tile = tile + count_of_tiles
                    data.append(new_tile)

                    temp.append(tile)
                else:
                    data.append(tile)
                    temp.append(tile)

            return data

        results = _split_string(man, 0)
        results += _split_string(pin, 36)
        results += _split_string(sou, 72)
        results += _split_string(honors, 108)

        return results

    @staticmethod
    def string_to_34_array(sou=None, pin=None, man=None, honors=None):
        """
        Method to convert one line string tiles format to the 34 array
        We need it to increase readability of our tests
        """
        results = TilesConverter.string_to_136_array(sou, pin, man, honors)
        results = TilesConverter.to_34_array(results)
        return results

    @staticmethod
    def find_34_tile_in_136_array(tile34, tiles):
        """
        Our shanten calculator will operate with 34 tiles format,
        after calculations we need to find calculated 34 tile
        in player's 136 tiles.

        For example we had 0 tile from 34 array
        in 136 array it can be present as 0, 1, 2, 3
        """
        if tile34 is None or tile34 > 33:
            return None

        tile = tile34 * 4

        possible_tiles = [tile] + [tile + i for i in range(1, 4)]

        found_tile = None
        for possible_tile in possible_tiles:
            if possible_tile in tiles:
                found_tile = possible_tile
                break

        return found_tile
