####################################################################
# Three-player hand by tsumo                                       #
####################################################################

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.tile import TilesConverter

tiles = TilesConverter.string_to_136_array(man="99", pin="123456789", sou="234")
win_tile = TilesConverter.string_to_136_array(sou="4")[0]
# west indicators make north the dora and the ura dora,
# so each extracted north is worth 3 han (nuki dora + dora + ura dora)
dora_indicators = TilesConverter.string_to_136_array(honors="3")
ura_dora_indicators = TilesConverter.string_to_136_array(honors="3")

config = HandConfig(
    is_riichi=True,
    is_tsumo=True,
    tsumi_number=1,
    num_nuki_dora=1,
    options=OptionalRules(is_three_player=True),
)
result = HandCalculator.estimate_hand_value(
    tiles,
    win_tile,
    dora_indicators=dora_indicators,
    ura_dora_indicators=ura_dora_indicators,
    config=config,
)

print(result.han, result.fu)
# each of the two other players pays 100 per honba, and the missing north seat's share is not paid (tsumo loss)
print(result.cost["main"] + result.cost["main_bonus"], result.cost["additional"] + result.cost["additional_bonus"])
print(result.cost["total"])
print(result.yaku)
