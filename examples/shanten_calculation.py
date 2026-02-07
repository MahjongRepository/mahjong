####################################################################
# Shanten calculation                                              #
####################################################################

from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

tiles = TilesConverter.string_to_34_array(man="13569", pin="123459", sou="443")
result = Shanten.calculate_shanten(tiles)

print(result)
