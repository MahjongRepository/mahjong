####################################################################
# Kazoe as a sanbaiman                                             #
####################################################################

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld
from mahjong.tile import TilesConverter

tiles = TilesConverter.string_to_136_array(man="222244466677788")
win_tile = TilesConverter.string_to_136_array(man="7")[0]
melds = [Meld(Meld.KAN, TilesConverter.string_to_136_array(man="2222"), False)]

dora_indicators = [
    TilesConverter.string_to_136_array(man="1")[0],
    TilesConverter.string_to_136_array(man="1")[0],
    TilesConverter.string_to_136_array(man="1")[0],
    TilesConverter.string_to_136_array(man="1")[0],
]

config = HandConfig(is_riichi=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_SANBAIMAN))
result = HandCalculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)

print(result.han, result.fu)
print(result.cost["main"])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
