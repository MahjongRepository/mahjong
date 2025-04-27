from tile import TilesConverter
from utils_for_tests import _hand, _make_meld, _string_to_136_tile

from mahjong.constants import EAST
from mahjong.hand_calculating.fu import FuCalculator
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.meld import Meld


def _get_win_group(hand, win_tile):
    return [x for x in hand if win_tile // 4 in x][0]


def test_chitoitsu_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="112244", man="115599", pin="6")
    win_tile = _string_to_136_tile(pin="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 1 == len(fu_details)
    assert {"fu": 25, "reason": FuCalculator.BASE} in fu_details
    assert fu == 25

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 1 == len(fu_details)
    assert {"fu": 25, "reason": FuCalculator.BASE} in fu_details
    assert fu == 25


def test_open_hand_base():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="22278", man="123456", pin="11")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))
    melds = [_make_meld(Meld.PON, sou="222")]

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config, melds=melds)
    assert 2 == len(fu_details)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.OPEN_PON} in fu_details
    assert fu == 30


def test_fu_based_on_win_group():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(man="234789", pin="1234566")
    win_tile = _string_to_136_tile(pin="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    win_groups = [x for x in hand if win_tile // 4 in x]

    # pinfu wait 4-5-6
    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, win_groups[0], config)
    assert fu == 30

    # pair wait 66
    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, win_groups[1], config)
    assert fu == 40


def test_open_hand_without_additional_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="23478", man="234567", pin="22")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))
    melds = [_make_meld(Meld.CHI, sou="234")]

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config, melds=melds)
    assert 2 == len(fu_details)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.HAND_WITHOUT_FU} in fu_details
    assert fu == 30


def test_open_hand_without_additional_fu_2():
    fu_calculator = FuCalculator()

    tiles = TilesConverter.string_to_136_array(sou="23478", man="234567", pin="22")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))
    melds = [_make_meld(Meld.CHI, sou="234")]

    config = HandConfig(options=OptionalRules(fu_for_open_pinfu=False))
    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config, melds=melds)
    assert 1 == len(fu_details)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details
    assert fu == 20


def test_tsumo_hand_base():
    fu_calculator = FuCalculator()
    config = HandConfig(is_tsumo=True)

    tiles = TilesConverter.string_to_136_array(sou="22278", man="123456", pin="11")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, _ = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details


def test_tsumo_hand_and_pinfu():
    fu_calculator = FuCalculator()
    config = HandConfig(is_tsumo=True)

    tiles = TilesConverter.string_to_136_array(sou="2278", man="123456", pin="123")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 1 == len(fu_details)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details
    assert fu == 20


def test_tsumo_hand_and_disabled_pinfu():
    fu_calculator = FuCalculator()
    config = HandConfig(is_tsumo=True, options=OptionalRules(fu_for_pinfu_tsumo=True))

    tiles = TilesConverter.string_to_136_array(sou="2278", man="123456", pin="123")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.TSUMO} in fu_details
    assert fu == 30


def test_tsumo_hand_and_not_pinfu():
    fu_calculator = FuCalculator()
    config = HandConfig(is_tsumo=True)

    tiles = TilesConverter.string_to_136_array(sou="2278", man="123456", pin="111")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.TSUMO} in fu_details
    assert fu == 30


def test_penchan_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    # 1-2-... wait
    tiles = TilesConverter.string_to_136_array(sou="12456", man="123456", pin="55")
    win_tile = _string_to_136_tile(sou="3")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.PENCHAN} in fu_details
    assert fu == 40

    # ...-8-9 wait
    tiles = TilesConverter.string_to_136_array(sou="34589", man="123456", pin="55")
    win_tile = _string_to_136_tile(sou="7")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.PENCHAN} in fu_details
    assert fu == 40


def test_kanchan_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="12357", man="123456", pin="55")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.KANCHAN} in fu_details
    assert fu == 40


def test_valued_pair_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="12378", man="123456", honors="11")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    valued_tiles = [EAST]
    fu_details, fu = fu_calculator.calculate_fu(
        hand,
        win_tile,
        _get_win_group(hand, win_tile),
        config,
        valued_tiles=valued_tiles,
    )
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.VALUED_PAIR} in fu_details
    assert fu == 40

    # double valued pair
    valued_tiles = [EAST, EAST]
    fu_details, fu = fu_calculator.calculate_fu(
        hand, win_tile, _get_win_group(hand, win_tile), config, valued_tiles=valued_tiles
    )
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 4, "reason": FuCalculator.DOUBLE_VALUED_PAIR} in fu_details
    assert fu == 40


def test_pair_wait_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="123678", man="123456", pin="1")
    win_tile = _string_to_136_tile(pin="1")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.PAIR_WAIT} in fu_details
    assert fu == 40


def test_closed_pon_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="22278", man="123456", pin="11")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 4, "reason": FuCalculator.CLOSED_PON} in fu_details
    assert fu == 40

    # when we ron on the third pon tile we consider pon as open
    tiles = TilesConverter.string_to_136_array(sou="22678", man="123456", pin="11")
    win_tile = _string_to_136_tile(sou="2")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 2, "reason": FuCalculator.OPEN_PON} in fu_details
    assert fu == 40


def test_closed_terminal_pon_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="11178", man="123456", pin="11")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 8, "reason": FuCalculator.CLOSED_TERMINAL_PON} in fu_details
    assert fu == 40

    # when we ron on the third pon tile we consider pon as open
    tiles = TilesConverter.string_to_136_array(sou="11678", man="123456", pin="11")
    win_tile = _string_to_136_tile(sou="1")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 4, "reason": FuCalculator.OPEN_TERMINAL_PON} in fu_details
    assert fu == 40


def test_closed_honor_pon_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="1178", man="123456", honors="111")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 8, "reason": FuCalculator.CLOSED_TERMINAL_PON} in fu_details
    assert fu == 40

    # when we ron on the third pon tile we consider pon as open
    tiles = TilesConverter.string_to_136_array(sou="11678", man="123456", honors="11")
    win_tile = _string_to_136_tile(honors="1")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 4, "reason": FuCalculator.OPEN_TERMINAL_PON} in fu_details
    assert fu == 40


def test_open_terminal_pon_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="2278", man="123456", honors="111")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))
    melds = [_make_meld(Meld.PON, honors="111")]

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config, melds=melds)
    assert 2 == len(fu_details)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 4, "reason": FuCalculator.OPEN_TERMINAL_PON} in fu_details
    assert fu == 30


def test_closed_kan_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="22278", man="123456", pin="11")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))
    melds = [_make_meld(Meld.KAN, sou="222", is_open=False)]

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config, melds=melds)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 16, "reason": FuCalculator.CLOSED_KAN} in fu_details
    assert fu == 50


def test_open_kan_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="22278", man="123456", pin="11")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))
    melds = [_make_meld(Meld.KAN, sou="222", is_open=True)]

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config, melds=melds)
    assert 2 == len(fu_details)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 8, "reason": FuCalculator.OPEN_KAN} in fu_details
    assert fu == 30


def test_closed_terminal_kan_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="2278", man="123456", pin="111")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))
    melds = [_make_meld(Meld.KAN, pin="111", is_open=False)]

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config, melds=melds)
    assert 2 == len(fu_details)
    assert {"fu": 30, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 32, "reason": FuCalculator.CLOSED_TERMINAL_KAN} in fu_details
    assert fu == 70


def test_open_terminal_kan_fu():
    fu_calculator = FuCalculator()
    config = HandConfig()

    tiles = TilesConverter.string_to_136_array(sou="2278", man="123456", pin="111")
    win_tile = _string_to_136_tile(sou="6")
    hand = _hand(TilesConverter.to_34_array(tiles + [win_tile]))
    melds = [_make_meld(Meld.KAN, pin="111", is_open=True)]

    fu_details, fu = fu_calculator.calculate_fu(hand, win_tile, _get_win_group(hand, win_tile), config, melds=melds)
    assert 2 == len(fu_details)
    assert {"fu": 20, "reason": FuCalculator.BASE} in fu_details
    assert {"fu": 16, "reason": FuCalculator.OPEN_TERMINAL_KAN} in fu_details
    assert fu == 40


def test_incorrect_fu_calculation_test_case_1():
    calculator = HandCalculator()

    tiles = TilesConverter.string_to_136_array(sou="11123456777", man="234")
    win_tile = _string_to_136_tile(sou="4")

    result = calculator.estimate_hand_value(tiles, win_tile, config=HandConfig(is_tsumo=True))
    assert result.fu == 30
    assert 3 == len(result.fu_details)
    assert {"fu": 20, "reason": FuCalculator.BASE} in result.fu_details
    assert {"fu": 8, "reason": FuCalculator.CLOSED_TERMINAL_PON} in result.fu_details
    assert {"fu": 2, "reason": FuCalculator.TSUMO} in result.fu_details


def test_incorrect_fu_calculation_test_case_2():
    calculator = HandCalculator()

    tiles = TilesConverter.string_to_136_array(pin="555", man="11112233444")
    melds = [_make_meld(Meld.CHI, man="123")]
    win_tile = _string_to_136_tile(man="1")

    result = calculator.estimate_hand_value(tiles, win_tile, melds=melds, config=HandConfig(is_houtei=True))
    assert result.fu == 30
