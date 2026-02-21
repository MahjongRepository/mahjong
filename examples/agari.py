####################################################################
# Agari (winning hand detection)                                   #
####################################################################

from mahjong.agari import Agari
from mahjong.tile import TilesConverter

# complete hand: 123s 456s 789s 123p 33m
tiles = TilesConverter.string_to_34_array(sou="123456789", pin="123", man="33")
print("Regular hand:", Agari.is_agari(tiles))

# incomplete hand: 123s 456s 789s 12345p
tiles = TilesConverter.string_to_34_array(sou="123456789", pin="12345")
print("Incomplete hand:", Agari.is_agari(tiles))

# seven pairs (chiitoitsu): 1133557799s 1199p
tiles = TilesConverter.string_to_34_array(sou="1133557799", pin="1199")
print("Seven pairs:", Agari.is_agari(tiles))

# thirteen orphans (kokushi): 19s 19p 199m 1234567z
tiles = TilesConverter.string_to_34_array(sou="19", pin="19", man="199", honors="1234567")
print("Kokushi:", Agari.is_agari(tiles))

# open hand with kan meld: 1111m 123456789p 22s
tiles = TilesConverter.string_to_34_array(man="1111", pin="123456789", sou="22")
open_set = [0, 0, 0, 0]  # kan of 1m (tile index 0 in 34-tile format)
print("Open hand with kan:", Agari.is_agari(tiles, [open_set]))
