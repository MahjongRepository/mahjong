from mahjong.tile import TilesConverter
from mahjong.meld import Meld
from mahjong.hand_calculating.divider import HandDivider


class TestMixin(object):

    def _string_to_open_34_set(self, sou='', pin='', man='', honors=''):
        open_set = TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)
        open_set[0] //= 4
        open_set[1] //= 4
        open_set[2] //= 4
        return open_set

    def _string_to_34_tile(self, sou='', pin='', man='', honors=''):
        item = TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)
        item[0] //= 4
        return item[0]

    def _string_to_34_array(self, sou='', pin='', man='', honors=''):
        return TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)

    def _string_to_136_array(self, sou='', pin='', man='', honors=''):
        return TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)

    def _string_to_136_tile(self, sou='', pin='', man='', honors=''):
        return TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)[0]

    def _to_34_array(self, tiles):
        return TilesConverter.to_34_array(tiles)

    def _to_string(self, tiles_136):
        return TilesConverter.to_one_line_string(tiles_136)

    def _hand(self, tiles, hand_index=0):
        hand_divider = HandDivider()
        return hand_divider.divide_hand(tiles, [], [])[hand_index]

    def _make_meld(self, meld_type, is_open=True, man='', pin='', sou='', honors=''):
        tiles = self._string_to_136_array(man=man, pin=pin, sou=sou, honors=honors)
        meld = Meld()
        meld.who = 0
        meld.type = meld_type
        meld.tiles = tiles
        meld.opened = is_open
        meld.called_tile = tiles[0]
        return meld
