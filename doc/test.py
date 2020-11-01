from mahjong.hand_calculating.hand import HandCalculator
from mahjong.meld import Meld
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

calculator = HandCalculator()


# useful helper
def print_hand_result(hand_result, language=None):
    print(hand_result.han, hand_result.fu)
    print(hand_result.cost)

    if not language:    # by default, use yaku.name
        print(hand_result.yaku)
    else:
        print([yaku.languages[language] for yaku in hand_result.yaku])

    for fu_item in hand_result.fu_details:
        print(fu_item)

    print('')


####################################################################
# Tanyao hand by ron                                               #
####################################################################


# we had to use all 14 tiles in that array
tiles = TilesConverter.string_to_136_array(man='112233', pin='667788', sou='44')
win_tile = TilesConverter.string_to_136_array(sou='4')[0]
config = HandConfig()
# config.is_dealer = True
config.is_tsumo = True
result = calculator.estimate_hand_value(tiles, win_tile, config=config)
print_hand_result(result, language='Chinese')
