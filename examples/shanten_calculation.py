####################################################################
# Shanten calculation                                              #
####################################################################

from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

# regular hand, 2 shanten
tiles = TilesConverter.string_to_34_array(man="13569", pin="123459", sou="443")
print("Regular hand shanten:", Shanten.calculate_shanten(tiles))

# tenpai (0 shanten, one tile away from winning)
tiles = TilesConverter.string_to_34_array(sou="111345677", pin="11", man="567")
print("Tenpai hand:", Shanten.calculate_shanten(tiles))

# complete hand (-1 shanten, already winning)
tiles = TilesConverter.string_to_34_array(sou="111234567", pin="11", man="567")
print("Complete hand:", Shanten.calculate_shanten(tiles))

# calculate shanten for specific hand forms
tiles = TilesConverter.string_to_34_array(sou="114477", pin="114477", man="76")
print("Chiitoitsu shanten:", Shanten.calculate_shanten_for_chiitoitsu_hand(tiles))

tiles = TilesConverter.string_to_34_array(sou="129", pin="19", man="19", honors="1234567")
print("Kokushi shanten:", Shanten.calculate_shanten_for_kokushi_hand(tiles))
