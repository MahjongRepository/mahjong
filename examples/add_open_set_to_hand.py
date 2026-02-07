####################################################################
# Add open set to hand                                             #
####################################################################

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld
from mahjong.tile import TilesConverter

# we had to use all 14 tiles in that array
tiles = TilesConverter.string_to_136_array(man="22444", pin="333567", sou="444")
win_tile = TilesConverter.string_to_136_array(sou="4")[0]
melds = [Meld(meld_type=Meld.PON, tiles=TilesConverter.string_to_136_array(man="444"))]

result = HandCalculator.estimate_hand_value(
    tiles,
    win_tile,
    melds=melds,
    config=HandConfig(options=OptionalRules(has_open_tanyao=True)),
)

print(result.han, result.fu)
print(result.cost["main"])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
