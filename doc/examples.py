from mahjong.hand_calculating.hand import HandCalculator
from mahjong.meld import Meld
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter
from mahjong.locale.text_reporter import TextReporter

calculator = HandCalculator()


# useful helper with locale
def print_hand_result(hand_result, locale='English'):   # 'Chinese' / 'Japanese'
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
tiles = TilesConverter.string_to_136_array(man='22444', pin='333567', sou='444')
win_tile = TilesConverter.string_to_136_array(sou='4')[0]

result = calculator.estimate_hand_value(tiles, win_tile)
print_hand_result(result)


####################################################################
# Tanyao hand by tsumo                                             #
####################################################################


result = calculator.estimate_hand_value(tiles, win_tile, config=HandConfig(is_tsumo=True))
print_hand_result(result)


####################################################################
# Add open set to hand                                             #
####################################################################


melds = [Meld(meld_type=Meld.PON, tiles=TilesConverter.string_to_136_array(man='444'))]

result = calculator.estimate_hand_value(tiles, win_tile, melds=melds, config=HandConfig(options=OptionalRules(has_open_tanyao=True)))
print_hand_result(result)


####################################################################
# Shanten calculation                                              #
####################################################################


shanten = Shanten()
tiles = TilesConverter.string_to_34_array(man='13569', pin='123459', sou='443')
result = shanten.calculate_shanten(tiles, [])

print(result)

####################################################################
# Kazoe as a sanbaiman                                             #
####################################################################


tiles = TilesConverter.string_to_136_array(man='22244466677788')
win_tile = TilesConverter.string_to_136_array(man='7')[0]
melds = [
    Meld(Meld.KAN, TilesConverter.string_to_136_array(man='2222'), False)
]

dora_indicators = [
    TilesConverter.string_to_136_array(man='1')[0],
    TilesConverter.string_to_136_array(man='1')[0],
    TilesConverter.string_to_136_array(man='1')[0],
    TilesConverter.string_to_136_array(man='1')[0],
]

config = HandConfig(is_riichi=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_SANBAIMAN))
result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
print_hand_result(result)


####################################################################
# Change the cost of yaku                                          #
####################################################################


config = HandConfig(is_renhou=True)
# renhou as an yakuman - old style
config.yaku.renhou.han_closed = 13

tiles = TilesConverter.string_to_136_array(man='22444', pin='333567', sou='444')
win_tile = TilesConverter.string_to_136_array(sou='4')[0]

result = calculator.estimate_hand_value(tiles, win_tile, config=config)
print_hand_result(result)
