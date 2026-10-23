####################################################################
# Three-player shanten calculation                                 #
####################################################################

from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

# 2m-8m are not used in three-player mahjong,
# so the spare 1m can form a sequence only in four-player mahjong
tiles = TilesConverter.string_to_34_array(man="1111", honors="111122233")
print("Four-player shanten:", Shanten.calculate_shanten(tiles))
print("Three-player shanten:", Shanten.calculate_shanten(tiles, is_three_player=True))
