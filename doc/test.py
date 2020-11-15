from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.locale.text_reporter import TextReporter
from mahjong.tile import TilesConverter

calculator = HandCalculator()


# useful helper
def print_hand_result(hand_result, locale='Chinese'):

    reporter = TextReporter(locale=locale)
    str_dict = reporter.report(hand_result)

    if hand_result.error:
        print(str_dict['error'])
    else:
        print(str_dict['fu_details'])
        print(str_dict['yaku'])
        print(str_dict['cost'])

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
print_hand_result(result, locale='Chinese')

####################################################################
# Bug: Yakuman and Non-yakuman Yakus should not add together       #
####################################################################


config = HandConfig(is_renhou=True)
# renhou as an yakuman - old style
config.yaku.renhou.han_closed = 13
# if you directly change this, it would lead to 32 total han, but it should be 13
dora_indicators = [
    TilesConverter.string_to_136_array(man='1')[0],
    TilesConverter.string_to_136_array(man='1')[0],
    TilesConverter.string_to_136_array(man='1')[0],
    TilesConverter.string_to_136_array(man='1')[0],
]
tiles = TilesConverter.string_to_136_array(man='22334466557788')
win_tile = TilesConverter.string_to_136_array(man='4')[0]

result = calculator.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators, config=config)
print_hand_result(result)

####################################################################
# Bug: Yakuman and Non-yakuman Yakus should not add together       #
####################################################################


config = HandConfig(is_renhou=True, options=OptionalRules(renhou_as_yakuman=True))
# renhou as an yakuman - old style

# This should be the correct way to count Renhou as Yakuman
dora_indicators = [
    TilesConverter.string_to_136_array(man='1')[0],
    TilesConverter.string_to_136_array(man='1')[0],
    TilesConverter.string_to_136_array(man='1')[0],
    TilesConverter.string_to_136_array(man='1')[0]
]

tiles = TilesConverter.string_to_136_array(man='22334466557788')
win_tile = TilesConverter.string_to_136_array(man='4')[0]

result = calculator.estimate_hand_value(tiles, win_tile, dora_indicators=dora_indicators, config=config)
print_hand_result(result)
