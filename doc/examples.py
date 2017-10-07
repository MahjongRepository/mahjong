from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.meld import Meld

calculator = HandCalculator()


def print_hand_result(hand_result):
    print(hand_result.han, hand_result.fu)
    print(hand_result.cost['main'])
    print(hand_result.yaku)
    for fu_item in hand_result.fu_details:
        print(fu_item)
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

result = calculator.estimate_hand_value(tiles, win_tile, is_tsumo=True)
print_hand_result(result)

####################################################################
# Add open set to hand                                             #
####################################################################

meld = Meld()
meld.type = Meld.PON
meld.tiles = TilesConverter.string_to_136_array(man='444')

result = calculator.estimate_hand_value(tiles, win_tile, melds=[meld], has_open_tanyao=True)
print_hand_result(result)
