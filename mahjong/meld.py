# -*- coding: utf-8 -*-
from mahjong.tile import TilesConverter


class Meld(object):
    CHI = 'chi'
    PON = 'pon'
    KAN = 'kan'
    CHANKAN = 'chankan'
    NUKI = 'nuki'

    who = None
    tiles = []
    type = None
    from_who = None
    called_tile = None
    # we need it to distinguish opened and closed kan
    opened = True

    def __str__(self):
        return 'Type: {}, Tiles: {} {}'.format(self.type, TilesConverter.to_one_line_string(self.tiles), self.tiles)

    # for calls in array
    def __repr__(self):
        return self.__str__()

    @property
    def tiles_34(self):
        return [x // 4 for x in self.tiles[:3]]
