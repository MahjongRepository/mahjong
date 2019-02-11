# -*- coding: utf-8 -*-
import unittest

from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.constants import EAST, SOUTH, WEST, NORTH, FIVE_RED_SOU, FIVE_RED_MAN, FIVE_RED_SOU
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.scores import Aotenjou
from mahjong.meld import Meld
from mahjong.tests_mixin import TestMixin
from mahjong.hand_calculating.yaku_config import YakuConfig
from mahjong.tile import TilesConverter


class AotenjouCalculationTestCase(unittest.TestCase, TestMixin):

    def test_aotenjou_hands(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='119', man='19', pin='19', honors='1234567')
        win_tile = self._string_to_136_tile(sou='1')

        result = hand.estimate_hand_value(tiles, win_tile, scores_calculator_factory=Aotenjou, config=self._make_hand_config(player_wind=EAST, round_wind=EAST, disable_double_yakuman=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 1)
        self.assertEqual(result.cost['main'], 7864400)

        tiles = self._string_to_136_array(man='234', honors='11122233344')
        win_tile = self._string_to_136_tile(man='2')
        melds = [
            self._make_meld(Meld.PON, honors='111'),
            self._make_meld(Meld.PON, honors='333'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 17)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 4)
        self.assertEqual(result.cost['main']+result.cost['additional'], 83886200)

        tiles = self._string_to_136_array(honors='11122233444777')
        win_tile = self._string_to_136_tile(honors='2')
        melds = [
            self._make_meld(Meld.PON, honors='444'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 31)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 6)
        self.assertEqual(result.cost['main']+result.cost['additional'], 1717986918400)

        # monster hand for fun

        tiles = self._string_to_136_array(honors='11133555666777')
        win_tile = self._string_to_136_tile(honors='3')

        melds = [
            self._make_meld(Meld.KAN, honors='1111', is_open=False),
            self._make_meld(Meld.KAN, honors='5555', is_open=False),
            self._make_meld(Meld.KAN, honors='6666', is_open=False),
            self._make_meld(Meld.KAN, honors='7777', is_open=False),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, dora_indicators=self._string_to_136_array(honors='22224444'),
            scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_riichi=True, is_tsumo=True, is_ippatsu=True, is_haitei=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 95)
        self.assertEqual(result.fu, 160)
        self.assertEqual(len(result.yaku), 11)
        self.assertEqual(result.cost['main']+result.cost['additional'], 101412048018258352119736256430200)


    def test_daisangen(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='11123', honors='555666777')
        win_tile = self._string_to_136_tile(sou='1')

        result = hand.estimate_hand_value(tiles, win_tile, scores_calculator_factory=Aotenjou, config=self._make_hand_config(player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.fu, 60)
        self.assertEqual(result.han, 20)
        self.assertEqual(len(result.yaku), 4)
        self.assertEqual(result.cost['main'], 1509949500)

    def test_shousuushii(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='123', honors='11122233444')
        win_tile = self._string_to_136_tile(honors='2')
        melds = [
            self._make_meld(Meld.PON, honors='444'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 18)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 5)
        self.assertEqual(result.cost['main']+result.cost['additional'], 209715200)

    def test_daisuushii(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='11', honors='111222333444')
        win_tile = self._string_to_136_tile(honors='2')
        melds = [
            self._make_meld(Meld.PON, honors='444'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 34)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 6)
        self.assertEqual(result.cost['main']+result.cost['additional'], 13743895347200)

    def test_tsuuiisou(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(honors='11133344455566')
        win_tile = self._string_to_136_tile(honors='6')
        melds = [
            self._make_meld(Meld.PON, honors='444'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 18)
        self.assertEqual(result.fu, 60)
        self.assertEqual(len(result.yaku), 5)
        self.assertEqual(result.cost['main']+result.cost['additional'], 251658400)

    def test_suuankou(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(man='11133355566688')
        win_tile = self._string_to_136_tile(man='8')

        result = hand.estimate_hand_value(tiles, win_tile, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 33)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 3)
        self.assertEqual(result.cost['main']+result.cost['additional'], 6871947673600)

    def test_chinroutou(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(man='111999', sou='11999', pin='111')
        win_tile = self._string_to_136_tile(sou='9')
        melds = [
            self._make_meld(Meld.PON, pin='111'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 15)
        self.assertEqual(result.fu, 50)
        self.assertEqual(len(result.yaku), 2)
        self.assertEqual(result.cost['main']+result.cost['additional'], 26214400)

    def test_chuuren_poutou(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(man='11112345678999')
        win_tile = self._string_to_136_tile(man='1')

        result = hand.estimate_hand_value(tiles, win_tile, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 16)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 3)
        self.assertEqual(result.cost['main']+result.cost['additional'], 31457400)

    def test_chuuren_poutou_inner(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(man='11123455678999')
        win_tile = self._string_to_136_tile(man='5')

        result = hand.estimate_hand_value(tiles, win_tile, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 27)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 2)
        self.assertEqual(result.cost['main']+result.cost['additional'], 85899346000)

    def test_suukantsu(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(man='111', sou='444', pin='999', honors='33322')
        win_tile = self._string_to_136_tile(honors='2')

        melds = [
            self._make_meld(Meld.KAN, man='1111'),
            self._make_meld(Meld.KAN, sou='4444'),
            self._make_meld(Meld.KAN, pin='9999'),
            self._make_meld(Meld.KAN, honors='3333'),
        ]

        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 13)
        self.assertEqual(result.fu, 80)
        self.assertEqual(len(result.yaku), 1)
        self.assertEqual(result.cost['main']+result.cost['additional'], 10485800)

    def test_daisharin(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(pin='22334455667788')
        win_tile = self._string_to_136_tile(pin='7')

        result = hand.estimate_hand_value(tiles, win_tile, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST, allow_daisharin=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 14)
        self.assertEqual(result.fu, 30)
        self.assertEqual(len(result.yaku), 2)
        self.assertEqual(result.cost['main']+result.cost['additional'], 7864400)

    def test_ryuisou(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou='223344666888', honors='66')
        win_tile = self._string_to_136_tile(sou='8')

        result = hand.estimate_hand_value(tiles, win_tile, scores_calculator_factory=Aotenjou, config=self._make_hand_config(is_tsumo=True, player_wind=EAST, round_wind=EAST, allow_daisharin=True))
        self.assertEqual(result.error, None)
        self.assertEqual(result.han, 15)
        self.assertEqual(result.fu, 40)
        self.assertEqual(len(result.yaku), 3)
        self.assertEqual(result.cost['main']+result.cost['additional'], 20971600)
