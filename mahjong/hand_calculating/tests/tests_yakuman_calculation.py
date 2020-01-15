# -*- coding: utf-8 -*-
import unittest

from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.hand_calculating.yaku_config import YakuConfig
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.meld import Meld
from mahjong.tests_mixin import TestMixin
from mahjong.tile import TilesConverter


class YakumanCalculationTestCase(unittest.TestCase, TestMixin):

    def setUp(self):
        self.config = YakuConfig()

    def test_is_tenhou(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tenhou=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chiihou(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_chiihou=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_daisangen(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='123', man='22', honors='555666777')
        self.assertTrue(self.config.daisangen.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='123', man='22', honors='555666777')
        win_tile = self._string_to_136_tile(honors='7')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

    def test_is_shosuushi(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='123', honors='11122233344')
        self.assertTrue(self.config.shosuushi.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='123', honors='11122233344')
        win_tile = self._string_to_136_tile(honors='4')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 60)
        self.assertEqual(len(result.yaku), 1)

    def test_is_daisuushi(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='22', honors='111222333444')
        self.assertTrue(self.config.daisuushi.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='22', honors='111222333444')
        win_tile = self._string_to_136_tile(honors='4')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 60)
        self.assertEqual(len(result.yaku), 1)

    def test_is_tsuisou(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(honors='11122233366677')
        self.assertTrue(self.config.tsuisou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(honors='11223344556677')
        self.assertTrue(self.config.tsuisou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(honors='1133445577', pin='88', sou='11')
        self.assertFalse(self.config.tsuisou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(honors='11223344556677')
        win_tile = self._string_to_136_tile(honors='7')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 25)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chinroto(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='111999', man='111999', pin='99')
        self.assertTrue(self.config.chinroto.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='111222', man='111999', pin='99')
        win_tile = self._string_to_136_tile(pin='9')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 60)
        self.assertEqual(len(result.yaku), 1)

    def test_is_kokushi(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='119', man='19', pin='19', honors='1234567')
        self.assertTrue(self.config.kokushi.is_condition_met(None, tiles))

        tiles = self._string_to_136_array(sou='119', man='19', pin='19', honors='1234567')
        win_tile = self._string_to_136_tile(sou='9')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 0)
        self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(sou='119', man='19', pin='19', honors='1234567')
        win_tile = self._string_to_136_tile(sou='1')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 0)
        self.assertEqual(len(result.yaku), 1)

    def test_is_ryuisou(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='22334466888', honors='666')
        self.assertTrue(self.config.ryuisou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(sou='22334466888', honors='666')
        win_tile = self._string_to_136_tile(honors='6')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

    def test_is_suuankou(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(sou='111444', man='333', pin='44555')
        win_tile = self._string_to_136_tile(sou='4')

        self.assertTrue(self.config.suuankou.is_condition_met(self._hand(tiles), win_tile, True))
        self.assertFalse(self.config.suuankou.is_condition_met(self._hand(tiles), win_tile, False))

        tiles = self._string_to_136_array(sou='111444', man='333', pin='44555')
        win_tile = self._string_to_136_tile(pin='5')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=False))
        self.assertNotEqual(result.han, 13)

        tiles = self._string_to_136_array(sou='111444', man='333', pin='44455')
        win_tile = self._string_to_136_tile(pin='5')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(man='33344455577799')
        win_tile = self._string_to_136_tile(man='9')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=False))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 26)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

    def test_is_chuuren_poutou(self):
        hand = HandCalculator()

        tiles = self._string_to_34_array(man='11112345678999')
        self.assertTrue(self.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(pin='11122345678999')
        self.assertTrue(self.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123345678999')
        self.assertTrue(self.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123445678999')
        self.assertTrue(self.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123455678999')
        self.assertTrue(self.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123456678999')
        self.assertTrue(self.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123456778999')
        self.assertTrue(self.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123456788999')
        self.assertTrue(self.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_34_array(sou='11123456789999')
        self.assertTrue(self.config.chuuren_poutou.is_condition_met(self._hand(tiles)))

        tiles = self._string_to_136_array(man='11123456789999')
        win_tile = self._string_to_136_tile(man='1')

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)

        daburi = [
            ['11122345678999', '2'],
            ['11123456789999', '9'],
            ['11112345678999', '1'],
        ]
        for hand_tiles, win_tile in daburi:
            tiles = self._string_to_136_array(man=hand_tiles)
            win_tile = self._string_to_136_tile(man=win_tile)

            result = hand.estimate_hand_value(tiles, win_tile)
            self.assertEqual(result.error, None)
            self.assertEqual(result.han, 26)
            self.assertEqual(len(result.yaku), 1)

        tiles = self._string_to_136_array(pin='11123456678999')
        win_tile = self._string_to_136_tile(pin='3')
        melds = [self._make_meld(Meld.KAN, pin='9999', is_open=False)]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 6)
        self.assertEqual(result.fu, 70)
        self.assertEqual(len(result.yaku), 1)

    def test_is_suukantsu(self):
        hand = HandCalculator()

        melds = [
            self._make_meld(Meld.KAN, sou='1111'),
            self._make_meld(Meld.KAN, sou='3333'),
            self._make_meld(Meld.KAN, pin='5555'),
            self._make_meld(Meld.CHANKAN, man='2222'),
        ]
        self.assertTrue(self.config.suukantsu.is_condition_met(None, melds))

        tiles = self._string_to_136_array(sou='111333', man='222', pin='44555')
        win_tile = self._string_to_136_tile(pin='4')
        melds = [
            self._make_meld(Meld.KAN, sou='1111'),
            self._make_meld(Meld.KAN, sou='3333'),
            self._make_meld(Meld.KAN, pin='5555'),
            self._make_meld(Meld.KAN, man='2222'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 70)
        self.assertEqual(len(result.yaku), 1)

    def test_disabled_double_yakuman(self):
        hand = HandCalculator()

        # kokushi
        tiles = self._string_to_136_array(sou='119', man='19', pin='19', honors='1234567')
        win_tile = self._string_to_136_tile(sou='1')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(disable_double_yakuman=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 0)
        self.assertEqual(len(result.yaku), 1)

        # suanko tanki
        tiles = self._string_to_136_array(sou='111444', man='333', pin='44455')
        win_tile = self._string_to_136_tile(pin='5')

        result = hand.estimate_hand_value(tiles, win_tile,
                                          config=self._make_hand_config(is_tsumo=True, disable_double_yakuman=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

        # chuuren poutou
        tiles = self._string_to_136_array(man='11122345678999')
        win_tile = self._string_to_136_tile(man='2')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(disable_double_yakuman=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 1)

        # daisushi
        tiles = self._string_to_136_array(sou='22', honors='111222333444')
        win_tile = self._string_to_136_tile(honors='4')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(disable_double_yakuman=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 60)
        self.assertEqual(len(result.yaku), 1)

    def test_sextuple_yakuman(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(honors='11122233344455')
        win_tile = self._string_to_136_tile(honors='5')

        config = self._make_hand_config(is_tenhou=True, disable_double_yakuman=False)

        result = hand.estimate_hand_value(tiles, win_tile, config=config)
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 78)
        self.assertEqual(result.cost['main'], 192000)

    def test_kokushi_musou_multiple_yakuman(self):
        hand_calculator = HandCalculator()

        # kokushi test

        tiles = TilesConverter.string_to_136_array(sou='19', pin='19', man='19', honors='12345677')
        win_tile = TilesConverter.string_to_136_array(honors='1')[0]

        hand_config = HandConfig(
            is_tsumo=True,
            is_tenhou=False,
            is_chiihou=False)

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 1)
        self.assertTrue(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 13)

        hand_config = HandConfig(
            is_tsumo=True,
            is_tenhou=True,
            is_chiihou=False
        )

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 2)
        self.assertTrue(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 26)

        hand_config = HandConfig(
            is_tsumo=True,
            is_tenhou=False,
            is_chiihou=True
        )

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 2)
        self.assertTrue(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 26)

        # double kokushi test

        tiles = TilesConverter.string_to_136_array(sou='19', pin='19', man='19', honors='12345677')
        win_tile = TilesConverter.string_to_136_array(honors='7')[0]

        hand_config = HandConfig(
            is_tsumo=True,
            is_tenhou=False,
            is_chiihou=False
        )

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 1)
        self.assertFalse(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 26)

        hand_config = HandConfig(
            is_tsumo=True,
            is_tenhou=True,
            is_chiihou=False
        )

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 2)
        self.assertFalse(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 39)

        hand_config = HandConfig(
            is_tsumo=True,
            is_tenhou=False,
            is_chiihou=True
        )

        hand_calculation = hand_calculator.estimate_hand_value(tiles, win_tile, config=hand_config)

        self.assertIsNone(hand_calculation.error)
        self.assertEqual(len(hand_calculation.yaku), 2)
        self.assertFalse(hand_config.yaku.kokushi in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.daburu_kokushi in hand_calculation.yaku)
        self.assertFalse(hand_config.yaku.tenhou in hand_calculation.yaku)
        self.assertTrue(hand_config.yaku.chiihou in hand_calculation.yaku)
        self.assertEqual(hand_calculation.han, 39)

    def test_is_renhou_yakuman(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123444', man='234456', pin='66')
        win_tile = self._string_to_136_tile(sou='4')

        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_renhou=True, renhou_as_yakuman=True)
        )
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(len(result.yaku), 1)

    def test_is_not_daisharin(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(pin='22334455667788')
        win_tile = self._string_to_136_tile(pin='8')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config())
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 11)
        self.assertEqual(len(result.yaku), 4)

    def test_is_daisharin(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(pin='22334455667788')
        win_tile = self._string_to_136_tile(pin='8')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(allow_daisharin=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(len(result.yaku), 1)
        self.assertEqual(result.yaku[0].name, 'Daisharin')

    def test_is_not_daichikurin(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(man='22334455667788')
        win_tile = self._string_to_136_tile(man='8')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(allow_daisharin=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 11)
        self.assertEqual(len(result.yaku), 4)

    def test_is_daichikurin(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(man='22334455667788')
        win_tile = self._string_to_136_tile(man='8')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(
            allow_daisharin=True, allow_daisharin_other_suits=True)
                                          )
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(len(result.yaku), 1)
        self.assertEqual(result.yaku[0].name, 'Daichikurin')

    def test_is_not_daisuurin(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='22334455667788')
        win_tile = self._string_to_136_tile(sou='8')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(allow_daisharin=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 11)
        self.assertEqual(len(result.yaku), 4)

    def test_is_daisuurin(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='22334455667788')
        win_tile = self._string_to_136_tile(sou='8')

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(
            allow_daisharin=True, allow_daisharin_other_suits=True)
                                          )
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(len(result.yaku), 1)
        self.assertEqual(result.yaku[0].name, 'Daisuurin')
